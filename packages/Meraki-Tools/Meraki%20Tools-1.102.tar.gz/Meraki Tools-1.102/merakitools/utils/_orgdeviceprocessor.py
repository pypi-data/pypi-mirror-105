"""
Proccess Meraki Data Model to find all devices with in an org and save informato to model
"""
import asyncio
import logging
import threading
import time
from datetime import datetime
from merakitools import const, lib, model
from .processor import proccess_network


class Org_device_proccesssor(threading.Thread):
	"""
    Setup meraki devices in data model in memory
    """
	
	def __init__(self, org_id):
		"""
        Init of Device Sync Sync Pocessor
        Args:
            org_id:ID or Org to be proccessed
        """
		threading.Thread.__init__(self)
		self.org_id = org_id
		self.networks = {}
	
	def run(self):
		start_time = time.perf_counter()
		threading.currentThread().setName(
			model.meraki_nets[self.org_id].name)
		asyncio.run(self._get_org_networks())
		if const.appcfg.debug:
			print(f'\tOrgName: {model.meraki_nets[self.org_id].name} Sync '
			      f'Started at: {start_time} '
			      f'Thread PID:{threading.currentThread().native_id}')
		
		devices = asyncio.run(self._get_org_devices())
		for device in devices:
			model.meraki_nets[self.org_id].devices.update(
					{device['serial']: model.Device(device, self.org_id)})
		
		asyncio.run(self._switch_procssor())
		
		model.meraki_nets[self.org_id].syncruntime = \
			time.perf_counter() - start_time
		model.meraki_nets[self.org_id].lastsync = datetime.utcnow()
		lib.store_cache(self.org_id,model.meraki_nets[self.org_id],'device_config')
		print(
			f'{lib.bc.OKBLUE} OrgName: {model.meraki_nets[self.org_id].name} finished device sync P{lib.bc.ENDC}')
	
	async def _get_org_networks(self):
		with lib.MerakiAsyncApi() as sdk:
			networks = await sdk.organizations.getOrganizationNetworks(
				self.org_id)
		for network in networks:
			self.networks.update({network['id']: network['tags']})
	
	async def _get_org_devices(self):
		with lib.MerakiAsyncApi() as sdk:
			return await sdk.organizations.getOrganizationDevices(
				self.org_id)
	
	def _setup_config_model(self, serial):
		device = model.meraki_nets[self.org_id].devices[serial]
		is_golden = False
		port_ids = {}
		if const.appcfg.tag_golden in self.networks[device.net_id]:
			is_golden = True
		if const.appcfg.tag_target in self.networks[device.net_id]:
			for port in device.config:
				for port_tags in port['tags']:
					if port_tags in const.appcfg.switch_port_tags:
						if is_golden:
							port.pop('portId')
							model.config_manager[
								const.appcfg.tag_golden].golden_port_config.update(
									{port_tags: port})
						else:
							if serial in model.config_manager[
									const.appcfg.tag_golden].target_switches[
									port_tags].keys():
								model.config_manager[
									const.appcfg.tag_golden].target_switches[
									port_tags][serial].append(
										port['portId'])
							else:
								model.config_manager[
									const.appcfg.tag_golden].target_switches[
									port_tags].update({serial: [port['portId']]})
								
								
	
	async def _switch_procssor(self):
		"""
        Function proccess Each swithin in an org and pulls configuation infroamtion down for each port on the switch
        The function will also place the port the data_model that is orginizaed by network tag, then poprt configuraiton tage
        Returns:

        """
		with lib.MerakiAsyncApi() as sdk:
			for device in model.meraki_nets[self.org_id].devices:
				serial = model.meraki_nets[self.org_id].devices[
					device].serial
				if model.meraki_nets[self.org_id].devices[
					device].prodect == 'switch':
					print(f'Getting Switch {serial} config')
					model.meraki_nets[self.org_id].devices[
						serial].config = await sdk.switch.getDeviceSwitchPorts(
							serial)
					self._setup_config_model(serial)
					print(f'Finished Switch {serial} config')
