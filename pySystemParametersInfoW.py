import ctypes
import ctypes.wintypes

class pySystemParametersInfoW():
#https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-systemparametersinfow
	def __init__(self):
		#Initialize instance of WinDLL User32 SystemParametersInfoW (64bit)
		#See SystemParametersInfoA for 32bit
		self.SystemParametersInfoW = ctypes.windll.user32.SystemParametersInfoW
		#define return type for function
		self.SystemParametersInfoW.restype = ctypes.c_bool

	#Pass an integer flags and a dictionary of flags, returns 
	#an array of dict keys values that matched
	def resolveFlags(self, flagsValue, flagsDict):
		resDict = {}
		for k,v in flagsDict.items():
			result = flagsValue & v
			if result == v:
				resDict[k] = v
		
		return resDict

	class uiAction():
		SPI_GETFILTERKEYS = 0x0032
		SPI_GETSTICKYKEYS = 0x003A
		SPI_GETTOGGLEKEYS = 0x0034
		SPI_GETKEYBOARDDELAY = 0x0016
		SPI_GETKEYBOARDSPEED = 0x000A
		SPI_GETMOUSE = 0x0003
		SPI_GETMOUSESPEED = 0x0070
		SPI_GETMOUSEKEYS = 0x0036

	'''
	Retrieves information about the FilterKeys accessibility feature. 
	The pvParam parameter must point to a FILTERKEYS structure that receives the information. 
	Set the cbSize member of this structure and the uiParam parameter to sizeof(FILTERKEYS). 
	'''

	class sFILTERKEYS(ctypes.Structure):
		_fields_ = [
			('cbSize', ctypes.c_uint),
			('dwFlags', ctypes.wintypes.DWORD),
			('iWaitMSec', ctypes.wintypes.DWORD),
			('iDelayMSec', ctypes.wintypes.DWORD),
			('iRepeatMSec', ctypes.wintypes.DWORD),
			('iBounceMSec', ctypes.wintypes.DWORD)
			]

	'''
	Contains information about the StickyKeys accessibility feature.
	typedef struct tagSTICKYKEYS {
	  UINT  cbSize;
	  DWORD dwFlags;
	} STICKYKEYS, *LPSTICKYKEYS;
	'''

	class sSTICKYKEYS(ctypes.Structure):
		_fields_ = [
			('cbSize', ctypes.c_uint),
			('dwFlags', ctypes.wintypes.DWORD)
			]

	'''
	Contains information about the MouseKeys accessibility feature.
	typedef struct tagMOUSEKEYS {
	  UINT  cbSize;
	  DWORD dwFlags;
	  DWORD iMaxSpeed;
	  DWORD iTimeToMaxSpeed;
	  DWORD iCtrlSpeed;
	  DWORD dwReserved1;
	  DWORD dwReserved2;
	} MOUSEKEYS, *LPMOUSEKEYS;
	'''

	class sMOUSEKEYS(ctypes.Structure):
		_fields_ = [
			('cbSize', ctypes.c_uint),
			('dwFlags', ctypes.wintypes.DWORD),
			('iMaxSpeed', ctypes.wintypes.DWORD),
			('iTimeToMaxSpeed', ctypes.wintypes.DWORD),
			('iCtrlSpeed', ctypes.wintypes.DWORD),
			('dwReserved1', ctypes.wintypes.DWORD),
			('dwReserved2', ctypes.wintypes.DWORD)
			]

	class sMOUSE(ctypes.Structure):
		_fields_ = [
			('MouseThreshold1', ctypes.c_int),
			('MouseThreshold2', ctypes.c_int),
			('MouseSpeed', ctypes.c_int),
			]

	class sKEYBOARDSPEED(ctypes.Structure):
		_fields_ = [
			('KeyboardSpeed', ctypes.wintypes.DWORD)
			]

	class sKEYBOARDDELAY(ctypes.Structure):
		_fields_ = [
			('KeyboardDelay', ctypes.c_int)
			]

	def SetProtoType(self, paramStruct):
		#define prototype for dll input params
		self.SystemParametersInfoW.argtypes = [
			ctypes.c_uint,
			ctypes.c_uint,
			ctypes.POINTER(paramStruct),
			ctypes.c_uint
			]

	def SPI_GETFILTERKEYS(self):
		WinParamName = 'SPI_GETFILTERKEYS - FilterKeys Keyboard Response'
		name = "FilterKeys"
		uiAction = self.uiAction.SPI_GETFILTERKEYS
		uiActionStruct = self.sFILTERKEYS()

		flagsDict = {
		"FKF_AVAILABLE": 0x00000002,
		"FKF_CLICKON": 0x00000040,
		"FKF_CONFIRMHOTKEY": 0x00000008,
		"FKF_FILTERKEYSON": 0x00000001,
		"FKF_HOTKEYACTIVE": 0x00000004,
		"FKF_HOTKEYSOUND": 0x00000010,
		"FKF_INDICATOR": 0x00000020
		}

		uiActionStruct.cbSize = ctypes.sizeof(uiActionStruct)
		self.SetProtoType(self.sFILTERKEYS)
			
		result = self.SystemParametersInfoW(
				uiAction,
				ctypes.sizeof(uiActionStruct),
				ctypes.byref(uiActionStruct),
				0
				)

		flagResult = self.resolveFlags(uiActionStruct.dwFlags, flagsDict)

		if result:
			print()
			print(f'{WinParamName}')
			print(f"\tdwFlags: {uiActionStruct.dwFlags}, Default: X")
			print(f"\t\tEnabled Features")
			for k in flagResult.keys():
				print(f"\t\t\t{k}")
			print(f"\t\tReference")
			print(f"\t\t\thttps://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-filterkeys")
			print(f"\tiWaitMSec: {uiActionStruct.iWaitMSec}, Min: >0, Max: 20000 (ms), Default: X")
			print(f"\tiDelayMSec: {uiActionStruct.iDelayMSec}, Min: >0, Max: 20000 (ms), Default: X")
			print(f"\tiRepeatMSec: {uiActionStruct.iRepeatMSec}, Min: >0, Max: 20000 (ms), Default: X")
			print(f"\tiBounceMSec: {uiActionStruct.iBounceMSec}, 0=Off, >1=On, Default: X")
			print()
			print(f"\tMicrosoft Remark:")
			print(f"\tThe iWaitMSec, iDelayMSec, and iRepeatMSec members work together\n\tto control the RepeatKeys and SlowKeys features.")
			print(f"\tIf BounceKeys is off (iBounceMSec is zero), the iWaitMSec,\n\tiDelayMSec, and iRepeatMSec must all be nonzero, and vice versa if it is On.")
		else:
			print()
			print(f'{WinParamName}')
			print(f"\tCould not get {name} data")
	
	def SPI_GETSTICKYKEYS(self):
		WinParamName =  'SPI_GETSTICKYKEYS - StickyKeys'
		name = 'StickyKeys'
		uiAction = self.uiAction.SPI_GETSTICKYKEYS
		uiActionStruct = self.sSTICKYKEYS()

		flagsDict = {
		"SKF_AUDIBLEFEEDBACK": 0x00000040,
		"SKF_AVAILABLE": 0x00000002,
		"SKF_CONFIRMHOTKEY": 0x00000008,
		"SKF_HOTKEYACTIVE": 0x00000004,
		"SKF_HOTKEYSOUND": 0x00000010,
		"SKF_INDICATOR": 0x00000020,
		"SKF_STICKYKEYSON": 0x00000001,
		"SKF_TRISTATE": 0x00000080,
		"SKF_TWOKEYSOFF":0x00000100,
		"SKF_LALTLATCHED": 0x10000000,
		"SKF_LCTLLATCHED": 0x04000000,
		"SKF_LSHIFTLATCHED": 0x01000000,
		"SKF_RALTLATCHED": 0x20000000,
		"SKF_RCTLLATCHED": 0x08000000,
		"SKF_LALTLOCKED": 0x00100000,
		"SKF_LCTLLOCKED": 0x00040000,
		"SKF_LSHIFTLOCKED": 0x00010000,
		"SKF_RALTLOCKED": 0x00200000,
		"SKF_RCTLLOCKED": 0x00080000,
		"SKF_RSHIFTLOCKED": 0x00020000,
		"SKF_LWINLATCHED": 0x40000000,
		"SKF_RWINLATCHED": 0x80000000,
		"SKF_LWINLOCKED": 0x00400000,
		"SKF_RWINLOCKED": 0x00800000
		}

		uiActionStruct.cbSize = ctypes.sizeof(uiActionStruct)
		self.SetProtoType(self.sSTICKYKEYS)
			
		result = self.SystemParametersInfoW(
				uiAction,
				ctypes.sizeof(uiActionStruct),
				ctypes.byref(uiActionStruct),
				0
				)

		flagResult = self.resolveFlags(uiActionStruct.dwFlags, flagsDict)

		if result:
			print()
			print(f'{WinParamName}')
			print(f"\tdwFlags: {uiActionStruct.dwFlags}")
			print(f"\t\tEnabled Features")
			for k in flagResult.keys():
				print(f"\t\t\t{k}")
			print(f"\t\tReference")
			print(f"\t\t\thttps://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-stickykeys")
		else:
			print()
			print(f'{WinParamName}')
			print(f"\tCould not get {name} data")

	def SPI_GETMOUSEKEYS(self):
		name = "MouseKeys"
		WinParamName = 'SPI_GETMOUSEKEYS - MouseKeys'
		uiAction = self.uiAction.SPI_GETMOUSEKEYS
		uiActionStruct = self.sMOUSEKEYS()

		uiActionStruct.cbSize = ctypes.sizeof(uiActionStruct)
		self.SetProtoType(self.sMOUSEKEYS)

		flagsDict = {
		"MKF_AVAILABLE": 0x00000002,
		"MKF_CONFIRMHOTKEY": 0x00000008,
		"MKF_HOTKEYACTIVE": 0x00000004,
		"MKF_HOTKEYSOUND": 0x00000010,
		"MKF_INDICATOR": 0x00000020,
		"MKF_LEFTBUTTONDOWN": 0x01000000,
		"MKF_LEFTBUTTONSEL": 0x10000000,
		"MKF_MODIFIERS": 0x00000040,
		"MKF_MOUSEKEYSON": 0x00000001,
		"MKF_MOUSEMODE": 0x80000000,
		"MKF_REPLACENUMBERS": 0x00000080,
		"MKF_RIGHTBUTTONDOWN": 0x02000000,
		"MKF_RIGHTBUTTONSEL": 0x20000000
		}
			
		result = self.SystemParametersInfoW(
				uiAction,
				ctypes.sizeof(uiActionStruct),
				ctypes.byref(uiActionStruct),
				0
				)
		
		#dwFlags is returned as an offset from 268435456 (0)
		dwFlags = uiActionStruct.dwFlags - 268435456
		flagResult = self.resolveFlags(dwFlags, flagsDict)

		if result:
			print()
			print(f'{WinParamName}')
			print(f"\tdwFlags: {dwFlags} ({uiActionStruct.dwFlags}), Default: 62")
			print(f"\t\tEnabled Features")
			for k in flagResult.keys():
				print(f"\t\t\t{k}")
			print(f"\t\tReference")
			print(f"\t\t\thttps://docs.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-mousekeys")
			print()
			print(f"\tiMaxSpeed: {uiActionStruct.iMaxSpeed}, MinTime: 10 (ms), MaxTime: 360 (ms), Default: 80")
			print(f"\tiTimeToMaxSpeed: {uiActionStruct.iTimeToMaxSpeed}, MinTime: 1000 (ms), MaxTime: 5000 (ms), Default: 3000")
			print(f"\tiCtrlSpeed: {uiActionStruct.iCtrlSpeed}, Min: 0, Max: N/A, Default: 0")
			print(f"\tdwReserved1: {uiActionStruct.dwReserved1}, Must be zero")
			print(f"\tdwReserved2: {uiActionStruct.dwReserved2}, Must be zero")
		else:
			print()
			print(f'{WinParamName}')
			print(f"\tCould not get {name} data")

	def SPI_GETMOUSE(self):
		WinParamName = 'SPI_GETMOUSE - Mouse Accel Thresholds and Enhanced Pointer Precision (EPP)'
		name = "MouseParams"
		uiAction = self.uiAction.SPI_GETMOUSE
		uiActionStruct = self.sMOUSE()
		self.SetProtoType(self.sMOUSE)
			
		result = self.SystemParametersInfoW(
				uiAction,
				ctypes.sizeof(uiActionStruct),
				ctypes.byref(uiActionStruct),
				0
				)

		if result:
			print()
			print(f'{WinParamName}')
			print(f"\tMouseThreshold1: {uiActionStruct.MouseThreshold1} \n\t\tEPP On Default: 6\n\t\tEPP Off Default: 0")
			print(f"\tMouseThreshold2: {uiActionStruct.MouseThreshold2} \n\t\tEPP On Default: 10\n\t\tEPP Off Default: 0")
			print(f"\tMouseSpeed: {uiActionStruct.MouseSpeed}, Enhanced Pointer Precision, On=1, Off=0, Default: On")
		else:
			print(f"\tCould not get {name} data")

	def SPI_GETKEYBOARDDELAY(self):
		WinParamName = 'SPI_GETKEYBOARDDELAY (Keyboard Settings: Delay)'
		name = "Keyboard Delay"
		uiAction = self.uiAction.SPI_GETKEYBOARDDELAY
		uiActionStruct = self.sKEYBOARDDELAY()
		self.SetProtoType(self.sKEYBOARDDELAY)
			
		result = self.SystemParametersInfoW(
				uiAction,
				ctypes.sizeof(uiActionStruct),
				ctypes.byref(uiActionStruct),
				0
				)

		if result:
			print()
			print(f'{WinParamName}')
			print(f"\tKeyboardDelay: {uiActionStruct.KeyboardDelay}, Min: 0 (250ms), Max: 3 (1 sec), Default: 1")
			print(f"\tMicrosoft Remark:")
			print(f"\tThe actual delay associated with each value may vary depending on the hardware.")
		else:
			print()
			print(f'{WinParamName}')
			print(f"\tCould not get {name} data")

	def SPI_GETKEYBOARDSPEED(self):
		WinParamName = 'SPI_GETKEYBOARDSPEED (Keyboard Settings: Speed)'
		name = "Keyboard Delay"
		uiAction = self.uiAction.SPI_GETKEYBOARDSPEED
		uiActionStruct = self.sKEYBOARDSPEED()
		self.SetProtoType(self.sKEYBOARDSPEED)

		result = self.SystemParametersInfoW(
				uiAction,
				ctypes.sizeof(uiActionStruct),
				ctypes.byref(uiActionStruct),
				0
				)

		if result:
			print()
			print(f'{WinParamName}')
			print(f"\tKeyboardSpeed: {uiActionStruct.KeyboardSpeed}, Min: 0 (2.5/sec), Max: 31 (30/sec), Default: 31")
			print()
			print(f"\tMicrosoft Remark:")
			print(f"\tThe actual repeat rates are hardware-dependent and may vary\n\tfrom a linear scale by as much as 20%.")
		else:
			print()
			print(f'{WinParamName}')
			print(f"\tCould not get {name} data")
