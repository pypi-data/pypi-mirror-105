# MIT License

# Copyright (c) 2021 kaalam.ai The Authors of Jazz

# Hosted at https://github.com/kaalam/kpipe


class KPipe():

	@staticmethod
	def info(calc_hashes = True):
		print('Called info(%s)' % (calc_hashes))
		return 0

	@staticmethod
	def make(force_rebuild = False):
		print('Called make(%s)' % (force_rebuild))
		return 0

	@staticmethod
	def help():
		print('Called help()')
		return 1
