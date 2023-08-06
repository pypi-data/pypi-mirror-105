# Copyright 2021 Patrick C. Tapping
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

__version__ = "0.2.0"

import os
import sys
import platform
import typing
import warnings
import logging
from enum import IntEnum
from ctypes import cdll, byref, c_int, c_longlong, c_double, c_wchar_p, c_void_p, POINTER, CFUNCTYPE, create_unicode_buffer
from ctypes.util import find_library

import numpy as np

log = logging.getLogger(__name__)
"""Logging output for use by this module."""

# Maximum size of strings sent/returned
STRING_BUFFER_SIZE = 1024
"""Buffer size to use when sending or receiveing strings from the camera."""

# Infinite timeout when waiting on image buffer
INFINITY = 0xFFFFFFFF
"""Value to indicate an infinite timeout value when waiting on an image buffer."""

# ctypes callback type (return type, argument types...)
_CALLBACK_FUNC = CFUNCTYPE(c_int, c_int, c_wchar_p, POINTER(c_longlong))

# Dictionary of features and their corresponding data type
FEATURES = {
    "AccumulateCount": "Integer",
    "AcquiredCount": "Integer",
    "AcquisitionStart": "Command",
    "AcquisitionStop": "Command",
    "AlternatingReadoutDirection": "Boolean",
    "AOIBinning": "Enumerated",
    "AOIHBin": "Integer",
    "AOIHeight": "Integer",
    "AOILayout": "Enumerated",
    "AOILeft": "Integer",
    "AOIStride": "Integer",
    "AOITop": "Integer",
    "AOIVBin": "Integer",
    "AOIWidth": "Integer",
    "AuxiliaryOutSource": "Enumerated",
    "AuxOutSourceTwo": "Enumerated",
    "BackoffTemperatureOffset": "Floating Point",
    "Baseline": "Integer",
    "BitDepth": "Enumerated",
    "BufferOverflowEvent": "Event",
    "BytesPerPixel": "Floating Point",
    "CameraAcquiring": "Boolean",
    "CameraDump": "Command",
    "CameraFamily": "String",
    "CameraMemory": "Integer",
    "CameraModel": "String",
    "CameraName": "String",
    "CameraPresent": "Boolean",
    "ColourFilter": "Enumerated",
    "ControllerID": "String",
    "CoolerPower": "Floating Point",
    "CycleMode": "Enumerated",
    "DDGIOCEnable": "Boolean",
    "DDGIOCNumberOfPulses": "Integer",
    "DDGIOCPeriod": "Integer",
    "DDGOutputDelay": "Integer",
    "DDGOutputEnable": "Boolean",
    "DDGOutputStepEnable": "Boolean",
    "DDGOpticalWidthEnable": "Boolean",
    "DDGOutputPolarity": "Enumerated",
    "DDGOutputSelector": "Enumerated",
    "DDGOutputWidth": "Integer",
    "DDGStepCount": "Integer",
    "DDGStepDelayCoefficientA": "Floating Point",
    "DDGStepDelayCoefficientB": "Floating Point",
    "DDGStepDelayMode": "Enumerated",
    "DDGStepEnabled": "Boolean",
    "DDGStepUploadProgress": "Integer",
    "DDGStepUploadRequired": "Boolean",
    "DDGStepWidthCoefficientA": "Floating Point",
    "DDGStepWidthCoefficientB": "Floating Point",
    "DDGStepWidthMode": "Enumerated",
    "DDGStepUploadModeValues": "Command",
    "DDR2Type": "String",
    "DeviceCount": "Integer",
    "DeviceVideoIndex": "Integer",
    "DisableShutter": "Boolean",
    "DriverVersion": "String",
    "ElectronicShutteringMode": "Enumerated",
    "EventEnable": "Boolean",
    "EventsMissedEvent": "Event",
    "EventSelector": "Enumerated",
    "ExposedPixelHeight": "Integer",
    "ExposureTime": "Floating Point",
    "ExposureEndEvent": "Event",
    "ExposureStartEvent": "Event",
    "ExternalIOReadout": "Boolean",
    "ExternalTriggerDelay": "Floating Point",
    "FanSpeed": "Enumerated",
    "FastAOIFrameRateEnabl": "Boolean",
    "FirmwareVersion": "String",
    "ForceShutterOpen": "Boolean",
    "FrameCount": "Integer",
    "FrameInterval": "Floating Point",
    "FrameIntervalTiming": "Boolean",
    "FrameRate": "Floating Point",
    "FullAOIControl": "Boolean",
    "GateMode": "Enumerated",
    "HeatSinkTemperature": "Floating Point",
    "I2CAddress": "Integer",
    "I2CByte": "Integer",
    "I2CByteCount": "Integer",
    "I2CByteSelector": "Integer",
    "I2CRead": "Command",
    "I2CWrite": "Command",
    "ImageSizeBytes": "Integer",
    "InputVoltage": "Floating Point",
    "InsertionDelay": "Enumerated",
    "InterfaceType": "String",
    "IOControl": "Enumerated",
    "IODirection": "Enumerated",
    "IOState": "Boolean",
    "IOInvert": "Boolean",
    "IOSelector": "Enumerated",
    "IRPreFlashEnable": "Boolean",
    "KeepCleanEnable": "Boolean",
    "KeepCleanPostExposureEnable": "Boolean",
    "LineScanSpeed": "Floating Point",
    "LUTIndex": "Integer",
    "LUTValue": "Integer",
    "MaxInterfaceTransferRate": "Floating Point",
    "MCPGain": "Integer",
    "MCPIntelligate": "Boolean",
    "MCPVoltage": "Integer",
    "MetadataEnable": "Boolean",
    "MetadataFrame": "Boolean",
    "MetadataFrameInfo": "Boolean", # Not in documentation, indicates whether frame info is contained in metadata.
    "MetadataTimestamp": "Boolean",
    "MicrocodeVersion": "String",
    "MultitrackBinned": "Boolean",
    "MultitrackCount": "Integer",
    "MultitrackEnd": "Integer",
    "MultitrackSelector": "Integer",
    "MultitrackStart": "Integer",
    "Overlap": "Boolean",
    "PIVEnable": "Boolean",
    "PixelCorrection": "Boolean", # Documentation says Enumerated on SimCam only, but implemented on Zyla and returns a boolean.
    "PixelEncoding": "Enumerated",
    "PixelHeight": "Floating Point",
    "PixelReadoutRate": "Enumerated",
    "PixelWidth": "Floating Point",
    "PortSelector": "Integer",
    "PreAmpGain": "Enumerated",
    "PreAmpGainChannel": "Enumerated",
    "PreAmpGainControl": "Enumerated",
    "PreAmpGainValue": "Integer",
    "PreAmpGainSelector": "Enumerated",
    "PreAmpOffsetValue": "Integer",
    "PreTriggerEnable": "Boolean",
    "ReadoutTime": "Floating Point",
    "RollingShutterGlobalClear": "Boolean",
    "RowNExposureEndEvent": "Event",
    "RowNExposureStartEvent": "Event",
    "RowReadTime": "Floating Point",
    "ScanSpeedControlEnable": "Boolean",
    "SensorCooling": "Boolean",
    "SensorHeight": "Integer",
    "SensorModel": "String",
    "SensorReadoutMode": "Enumerated",
    "SensorType": "String",  # Documentation says Enumerated on Apogee only, but implemented on Zyla and returns a string.
    "SensorTemperature": "Floating Point",
    "SensorWidth": "Integer",
    "SerialNumber": "String",
    "ShutterAmpControl": "Boolean",
    "ShutterMode": "Enumerated",
    "ShutterOutputMode": "Enumerated",
    "ShutterState": "Boolean",
    "ShutterStrobePeriod": "Floating Point",
    "ShutterStrobePosition": "Floating Point",
    "ShutterTransferTime": "Floating Point",
    "SimplePreAmpGainControl": "Enumerated",
    "SoftwareTrigger": "Command",
    "SoftwareVersion": "String",
    "SpuriousNoiseFilter": "Boolean",
    "StaticBlemishCorrection": "Boolean",
    "SynchronousTriggering": "Boolean",
    "TargetSensorTemperature": "Floating Point",
    "TemperatureControl": "Enumerated",
    "TemperatureStatus": "Enumerated",
    "TimestampClock": "Integer",
    "TimestampClockFrequency": "Integer",
    "TimestampClockReset": "Command",
    "TransmitFrames": "Boolean",
    "TriggerMode": "Enumerated",
    "UsbProductId": "Integer",
    "UsbDeviceId": "Integer",
    "VerticallyCentreAOI": "Boolean"
}
"""
Dictionary containing valid camera feature strings and their corresponding data type.
"""


class Andor3():
    """
    Initialise the Andor SDK3 and attempt to open a connection to a camera.

    If ``device_index`` is None, camera initialisation won't be attempted, however the number of
    cameras attached may be queried with :data:`~Andor3.device_count`, and a camera subsequently opened
    with :meth:`open`.
    
    :param device_index: Index (zero-based) of attached camera to open.
    """

    def __init__(self, device_index:int=0):

        # Andor3 library only exists for Linux or Windows
        self.dll = None
        """Reference to the python ctypes library in use."""
        if platform.system() == "Windows":
            libname = "atcore.dll"
        elif platform.system() == "Linux":
            libname = "libatcore.so.3"
        else:
            raise EnvironmentError("Did not detect a Windows or Linux operating system!")

        # Find and load the Andor library
        dll_path = None
        try:
            # Use system installed library if available
            log.debug(f"Searching for Andor3 library in system paths...")
            self.dll = cdll.LoadLibrary(libname)
            dll_path = os.path.dirname(find_library(libname))
        except:
            pass
        
        # If that didn't work, try some other common locations
        if self.dll is None and platform.system() == "Windows":
            for loc in (os.path.join(os.environ["ProgramFiles"], "Andor Driver Pack 3"),
                        os.path.join(os.environ["ProgramFiles"], "Andor SOLIS"),
                        os.path.join(os.environ["ProgramFiles"], "National Instruments", "LabVIEW")):    
                try:
                    log.debug(f"Searching for Andor3 library in {loc}...")
                    self.dll = cdll.LoadLibrary(os.path.join(loc, libname))
                    # If that worked, add location to path so atcore.dll can find the other dlls it needs.
                    os.environ["PATH"] = f"{os.environ['PATH']}{os.pathsep}{loc}"
                    dll_path = loc
                    break
                except:
                    pass
        
        # Check current directory
        if self.dll is None:
            try:
                loc = os.path.abspath(".")
                log.debug(f"Searching for Andor3 library in {loc}...")
                self.dll = cdll.LoadLibrary(os.path.join(loc, libname))
                # Don't need to add to paths on Windows (atcore.dll must search in current dir)
                # On Linux, maybe need to add to LD_LIBRARY_PATH or something?
                dll_path = loc
            except:
                pass
        
        # Hopefully we found the library somewhere!
        if self.dll is None:
            raise RuntimeError(f"Couldn't find the Andor3 shared library '{libname}'")
        log.info(f"Initialising Andor3 library found at {dll_path}{os.sep}{libname}...")
        
        # Initialise library
        error = self.dll.AT_InitialiseLibrary()
        if not error == AT_ERR.SUCCESS:
            raise AndorError(error)
        
        # Get SDK version number
        software_version = create_unicode_buffer(STRING_BUFFER_SIZE)
        error = self.dll.AT_GetString(AT_HANDLE.SYSTEM, "SoftwareVersion", byref(software_version))
        if not error == AT_ERR.SUCCESS:
            self.dll.AT_FinaliseLibrary()
            raise AndorError(error)
        self.software_version = software_version.value
        log.debug(f"Andor3 library version {self.software_version}")
        """Version number of the SDK3 library in use."""

        # Get device count
        if device_index is None: device_index = -1
        device_count = c_int()
        error = self.dll.AT_GetInt(AT_HANDLE.SYSTEM, "DeviceCount", byref(device_count))
        if not error == AT_ERR.SUCCESS:
            self.dll.AT_FinaliseLibrary()
            raise AndorError(error)
        if device_count.value < 1 or device_index + 1 > device_count.value:
            # Raise error if no cameras found, or not enough cameras
            self.dll.AT_FinaliseLibrary()
            raise AndorError(AT_ERR.DEVICENOTFOUND)
        self.device_count = device_count.value
        """Number of detected cameras attached to the system."""
        log.debug(f"Detected {self.device_count} device{'s' if self.device_count > 1 else ''}")
        self.camera_handle = AT_HANDLE.UNINITIALISED
        """The "camera handle" used by the SDK to identify the currently opened camera."""

        # If a device_index is given, attempt to open the camera
        if device_index >= 0:
            try:
                self.open(device_index)
            except:
                self.dll.AT_FinaliseLibrary()
                raise
        
        # Our own record of registered feature callbacks
        self._callbacks = dict()

        # Block of memory for image buffer(s)
        self._image_buffer = None
        # Properties of images at the time the image buffer was created
        self._image_properties = None

    def open(self, device_index:int=0) -> None:
        """
        Open an attached camera device by its numerical device index.

        :param device_index: Index (zero-based) of the camera to open.
        """
        # Close any currently open camera
        self.close()
        # Attempt open of new camera
        log.debug(f"Opening connection to camera #{device_index}...")
        camera_handle = c_int()
        error = self.dll.AT_Open(device_index, byref(camera_handle))
        if not error == AT_ERR.SUCCESS:
            raise AndorError(error)
        self.camera_handle = camera_handle.value
        log.debug(f"Camera assigned handle {self.camera_handle}")


    def close(self) -> None:
        """
        Close any currently opened camera.
        """
        if not self.camera_handle == AT_HANDLE.UNINITIALISED:
            error = self.dll.AT_Close(self.camera_handle)
            if not error == AT_ERR.SUCCESS:
                raise AndorError(error)
            self.camera_handle = AT_HANDLE.UNINITIALISED
            log.debug("Closed connection to camera")

    def __del__(self):
        if not self.camera_handle == AT_HANDLE.UNINITIALISED:
            self.dll.AT_Close(self.camera_handle)
        self.dll.AT_FinaliseLibrary()

    def isImplemented(self, feature: str) -> bool:
        """
        Check if the given feature is implemented on the currently opened camera.

        See the :data:`FEATURES` dictionary for possible ``feature`` values.
        
        :param feature: String describing the camera feature.
        :returns: ``True`` if feature is implemented, or ``False`` otherwise.
        """
        result = c_int()
        error = self.dll.AT_IsImplemented(self.camera_handle, feature, byref(result))
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
        return bool(result.value)
    
    def isReadable(self, feature: str) -> bool:
        """
        Check if the given feature is currently readable.

        See the :data:`FEATURES` dictionary for possible ``feature`` values.
        
        :param feature: String describing the camera feature.
        :returns: ``True`` if feature is readable, or ``False`` otherwise.
        """
        result = c_int()
        error = self.dll.AT_IsReadable(self.camera_handle, feature, byref(result))
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
        return bool(result.value)
    
    def isWritable(self, feature: str) -> bool:
        """
        Check if the given feature is currently writable.

        See the :data:`FEATURES` dictionary for possible ``feature`` values.
        
        :param feature: String describing the camera feature.
        :returns: ``True`` if feature is writable, or ``False`` otherwise.
        """
        result = c_int()
        error = self.dll.AT_IsWritable(self.camera_handle, feature, byref(result))
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
        return bool(result.value)
    
    def isReadOnly(self, feature: str) -> bool:
        """
        Check if the given feature is read-only.

        See the :data:`FEATURES` dictionary for possible ``feature`` values.
        
        :param feature: String describing the camera feature.
        :returns: ``True`` if feature is read-only, or ``False`` otherwise.
        """
        result = c_int()
        error = self.dll.AT_IsReadOnly(self.camera_handle, feature, byref(result))
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
        return bool(result.value)

    def setInt(self, feature: str, value: int) -> None:
        """
        Set the value for a given integer feature.

        See the :data:`FEATURES` dictionary for possible ``feature`` values.
        
        :param feature: String describing the camera feature.
        :param value: New value for the feature.
        """
        error = self.dll.AT_SetInt(self.camera_handle, feature, c_longlong(value))
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
    
    def getInt(self, feature: str) -> int:
        """
        Get the value for a given integer feature.

        See the :data:`FEATURES` dictionary for possible ``feature`` values.
        
        :param feature: String describing the camera feature.
        :returns: Value for the feature.
        """
        result = c_longlong()
        error = self.dll.AT_GetInt(self.camera_handle, feature, byref(result))
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
        return result.value
    
    def getIntMin(self, feature: str) -> int:
        """
        Get the minimum allowed value for a given integer feature.

        See the :data:`FEATURES` dictionary for possible ``feature`` values.
        
        :param feature: String describing the camera feature.
        :returns: Minimum allowed value for the feature.
        """
        result = c_longlong()
        error = self.dll.AT_GetIntMin(self.camera_handle, feature, byref(result))
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
        return result.value

    def getIntMax(self, feature: str) -> int:
        """
        Get the maximum allowed value for a given integer feature.

        See the :data:`FEATURES` dictionary for possible ``feature`` values.
        
        :param feature: String describing the camera feature.
        :returns: Maximum allowed value for the feature.
        """
        result = c_longlong()
        error = self.dll.AT_GetIntMax(self.camera_handle, feature, byref(result))
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
        return result.value

    def setFloat(self, feature: str, value: float) -> None:
        """
        Set the value for a given floating point number feature.

        See the :data:`FEATURES` dictionary for possible ``feature`` values.
        
        :param feature: String describing the camera feature.
        :param value: New value for the feature.
        """
        error = self.dll.AT_SetFloat(self.camera_handle, feature, c_double(value))
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
    
    def getFloat(self, feature: str) -> float:
        """
        Get the minimum allowed value for a given floating point number feature.

        See the :data:`FEATURES` dictionary for possible ``feature`` values.
        
        :param feature: String describing the camera feature.
        :returns: Minimum allowed value for the feature.
        """
        result = c_double()
        error = self.dll.AT_GetFloat(self.camera_handle, feature, byref(result))
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
        return result.value
    
    def getFloatMin(self, feature: str) -> float:
        """
        Get the minimum allowed value for a given floating point number feature.

        See the :data:`FEATURES` dictionary for possible ``feature`` values.
        
        :param feature: String describing the camera feature.
        :returns: Minimum allowed value for the feature.
        """
        result = c_double()
        error = self.dll.AT_GetFloatMin(self.camera_handle, feature, byref(result))
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
        return result.value

    def getFloatMax(self, feature: str) -> float:
        """
        Get the maximum allowed value for a given floating point number feature.

        See the :data:`FEATURES` dictionary for possible ``feature`` values.
        
        :param feature: String describing the camera feature.
        :returns: Maximum allowed value for the feature.
        """
        result = c_double()
        error = self.dll.AT_GetFloatMax(self.camera_handle, feature, byref(result))
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
        return result.value

    def setBool(self, feature: str, value: bool) -> None:
        error = self.dll.AT_SetBool(self.camera_handle, feature, c_int(value))
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
    
    def getBool(self, feature: str) -> bool:
        result = c_int()
        error = self.dll.AT_GetBool(self.camera_handle, feature, byref(result))
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
        return bool(result.value)
    
    def setEnumIndex(self, feature: str, value: int) -> None:
        error = self.dll.AT_SetEnumIndex(self.camera_handle, feature, c_int(value))
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
    
    def setEnumString(self, feature: str, value: str) -> None:
        error = self.dll.AT_SetEnumString(self.camera_handle, feature, value)
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
    
    def getEnumIndex(self, feature: str) -> int:
        result = c_int()
        error = self.dll.AT_GetEnumIndex(self.camera_handle, feature, byref(result))
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
        return result.value
    
    def getEnumCount(self, feature: str) -> int:
        result = c_int()
        error = self.dll.AT_GetEnumCount(self.camera_handle, feature, byref(result))
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
        return result.value
    
    def isEnumIndexAvailable(self, feature: str, index: int) -> bool:
        result = c_int()
        error = self.dll.AT_IsEnumIndexAvailable(self.camera_handle, feature, index, byref(result))
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
        return bool(result.value)
    
    def isEnumIndexImplemented(self, feature: str, index: int) -> bool:
        result = c_int()
        error = self.dll.AT_IsEnumIndexImplemented(self.camera_handle, feature, index, byref(result))
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
        return bool(result.value)
    
    def getEnumStringByIndex(self, feature: str, index: int) -> str:
        result = create_unicode_buffer(STRING_BUFFER_SIZE)
        error = self.dll.AT_GetEnumStringByIndex(self.camera_handle, feature, index, byref(result), STRING_BUFFER_SIZE)
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
        return result.value
    
    def command(self, feature: str) -> None:
        """
        Activate a command type camera feature.

        A command is a camera feature which takes no parameters, for example ``"AcquisitionStart"``, or ``"SoftwareTrigger"``.

        :param feature: String describing the camera feature.
        """
        error = self.dll.AT_Command(self.camera_handle, feature)
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
    
    def setString(self, feature: str, value: str) -> None:
        error = self.dll.AT_SetString(self.camera_handle, feature, value)
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
    
    def getString(self, feature: str) -> str:
        result = create_unicode_buffer(STRING_BUFFER_SIZE)
        error = self.dll.AT_GetString(self.camera_handle, feature, byref(result), STRING_BUFFER_SIZE)
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
        return result.value

    def getStringMaxLength(self, feature: str) -> int:
        result = c_int()
        error = self.dll.AT_GetStringMaxLength(self.camera_handle, feature, byref(result))
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
        return result.value
    
    # I think the Andor library ends up calling the callback function twice when triggered, it's not my fault!
    def registerFeatureCallback(self, feature: str, callback: typing.Callable, args:tuple=(), kwargs:dict={}) -> None:
        """
        Register a method to call when the selected event occurs.

        The Andor library will call the callback immediately so that the callback handler can
        perform any action on the initial value etc.
        However, I think the Andor library ends up calling the callback function twice when
        triggered which is likely a bug.

        :param feature: String describing the feature event.
        :param callback: Method to call when event occurs.
        :param args: Tuple of positional arguments to pass to ``callback``.
        :param kwargs: Dictionary of keyword arguments to pass to ``callback``.
        """
        # Keys for callback dict are the hash of the tuple of (feature, callback)
        # This means can't use the same feature and function with different calling parameters though.
        # Would we ever want to do that? Maybe. Would instead need to make a unique identifier and return it.
        key = hash((feature, callback))
        if key not in self._callbacks:
            # Make a ctypes wrapper function to pass to the Andor library
            cfunc = _CALLBACK_FUNC(self._feature_callback)
            # We could assume that nothing in the Andor libraries would try to dereference our void pointer,
            # then could just pass the key as is. But to be safe, we'll make a real c_longlong of the key and keep it around.
            ckey = c_longlong(key)
            # Add everything to our dict of callbacks
            self._callbacks[key] = (cfunc, ckey, feature, callback, args, kwargs)
            # Register with Andor library.
            # Note that callback will be called immediately once.
            error = self.dll.AT_RegisterFeatureCallback(self.camera_handle, feature, cfunc, byref(ckey))
            if not error == AT_ERR.SUCCESS:
                self._callbacks.pop(key)
                raise AndorError(error)
        else:
            log.warn(f"Feature callback for \"{feature}\" already registered to the function \"{callback}\"")
        
    def _feature_callback(self, handle, feature, key_pointer):
        # Dereference the pointer to the c_longlong and get it's value
        key = key_pointer.contents.value
        # Grab everything from our callback dict
        _, _, feature, callback, args, kwargs = self._callbacks[key]
        # Could actually check the camera handle is the one we are currently using
        # and that the feature strings match what we expect. They're probably fine...
        # Call the requested python function and pass given parameters
        callback(*args, **kwargs)
        return 0

    def unregisterFeatureCallback(self, feature: str, callback:typing.Callable) -> None:
        """
        Unregister a previously registered callback method.

        The ``callback`` must have been previously registered to the ``feature`` using
        :meth:`registerFeatureCallback`.

        :param feature: String describing the feature event.
        :param callback: Method previously registered for callbacks.
        """
        # Generate dict key
        key = hash((feature, callback))
        if key in self._callbacks:
            # Grab everything from our callback dict and remove the entry
            cfunc, ckey, feature, callback, _, _ = self._callbacks.pop(key)
            # Unregister with Andor library.
            error = self.dll.AT_UnregisterFeatureCallback(self.camera_handle, feature, cfunc, byref(ckey))
            if not error == AT_ERR.SUCCESS:
                raise AndorError(error)
        else:
            log.warn(f"Feature callback for \"{feature}\" was not registered to the function \"{callback}\"")

    def queueBuffer(self, count:int=1) -> None:
        """
        Prepare a memory buffer for image storage by the Andor SDK3.

        Note that any previously prepared buffers will be destroyed.

        Multiple bufferes may be prepared in a single call by using the ``count`` parameter.

        :param count: Number of buffers to prepare.
        """
        # First, clear any existing buffer
        self.flush()
        self._image_buffer = None
        self._image_properties = None
        # Andor library wants the buffers to be aligned to 8-byte memory locations.
        # I think numpy does this anyway, but can enforce it with some array slicing.
        # Image size includes optional metadata
        imgsize = self.getInt("ImageSizeBytes")        
        # Padding required at end of image to make imgsize a multiple of 8
        postpad = (8 - imgsize%8)%8
        # Allocate a buffer big enough so can offset if needed
        buffer = np.empty(count*(imgsize + postpad) + 8, dtype=np.uint8)
        # Offset from start of buffer to enforce 8 byte alignment
        offset = -buffer.ctypes.data%8
        self._image_buffer = buffer[offset:offset + count*(imgsize + postpad)]
        # Queue up the buffer(s) in the Andor library
        for p in range(self._image_buffer.ctypes.data, self._image_buffer.ctypes.data + self._image_buffer.size, imgsize + postpad):
            error = self.dll.AT_QueueBuffer(self.camera_handle, c_void_p(p), imgsize)
            if not error == AT_ERR.SUCCESS:
                self._image_buffer = None
                self._image_properties = None
                raise AndorError(error)
        # Get the current image properties, which can be used for decoding the raw image data later
        self._image_properties = {
            "metadata" : self.MetadataEnable,
            #"metadata_frame_info" : self.MetadataFrameInfo,
            "metadata_timestamp" : self.MetadataTimestamp,
            "metadata_frame" : self.MetadataFrame,
            "encoding" : self.PixelEncoding[1],
            "size" : imgsize,
            "width" : self.AOIWidth,
            "height" : self.AOIHeight,
            "stride" : self.AOIStride
        }

    def waitBuffer(self, timeout:int=INFINITY, copy:bool=False, requeue:bool=False) -> np.ndarray:
        """
        Wait for the Andor SDK3 to fill a previously prepared memory buffer and return the data.

        The ``timeout`` parameter specifies how long to wait (in milliseconds) for the buffer to
        be filled.
        A value of :data:`INFINITY` will wait indefinitely, while a value of zero will return
        immediately if there is no buffered currently filled with new image data.

        Setting the ``copy=True`` parameter will make a copy of the data from the memory buffer,
        otherwise only a reference to the buffer memory will be used. Copying is slower (and uses
        more memory), but may be useful if the memory buffer is at risk of being overwritten by
        new data, for example if ``requeue=True`` is set, or :meth:`queueBuffer` is called to
        create a new buffer space.

        Setting the ``requeue=True`` parameter will allow the Andor SDK3 to re-use the buffer space
        in a circular-buffer type arrangement.
        It's may be a good idea to also set ``copy=True`` to ensure the data isn't overwritten by
        the camera before it's used.

        The raw data is returned as a 1-dimensional numpy array of bytes (uint8).

        :param timeout: Timeout (in milliseconds).
        :param copy: Copy the image data instead of returning a reference.
        :param requeue: Re-queue the image buffer for use again.
        :returns: 1-dimensional numpy array of raw image data.
        """
        data_pointer = c_void_p()
        data_size = c_int()
        error = self.dll.AT_WaitBuffer(self.camera_handle, byref(data_pointer), byref(data_size), timeout)
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
        # Compute slice indices
        start_i = data_pointer.value - self._image_buffer.ctypes.data
        stop_i = start_i + data_size.value
        # Get slice from image buffer
        data = self._image_buffer[start_i:stop_i]
        if copy:
            # Copy data out of buffer before it is requeued and the memory potentially overwritten
            data = data.copy()
        # Requeue the same buffer space if requested.
        if requeue:
            error = self.dll.AT_QueueBuffer(self.camera_handle, data_pointer, data_size)
            if not error == AT_ERR.SUCCESS: raise AndorError(error)
        return data
    
    def flush(self):
        """
        Destroy any existing image buffers.
        """
        self._image_buffer = None
        error = self.dll.AT_Flush(self.camera_handle)
        if not error == AT_ERR.SUCCESS: raise AndorError(error)

    def get_feature(self, feature:str, errors="warn"):
        """
        Queries the value of a camera ``feature``, without needing to know the particular data type.

        Internally, calls the appropriate ``getBool``, ``getInt``, ``getFloat``, ``getString`` or ``getEnum`` for ``feature`` and returns the value.
        Enum types return a tuple of (index, string).

        See :data:`FEATURES` for a list of camera features.

        By default any errors when querying the value are warned about (``errors="warn"``).
        To instead raise exceptions, set ``errors="raise"``.
        To silence errors completely, set ``errors="ignore"``.
        If a value is unable to be queried and errors are ignored, ``None`` will be returned.

        :param feature: String matching the camera feature to query.
        :param errors: Action to take on errors, either ``ignore``, ``warn``, or ``raise``.
        :returns: Value of the requested feature.
        """
        result = None
        try:
            if feature not in FEATURES:
                raise RuntimeError(f"Unknown feature '{feature}'.")
            if FEATURES[feature] in ("Command", "Event"):
                # Commands don't have values.
                # Events, although documented as integer types, are only used to register callbacks.
                raise RuntimeError(f"Attempted to get the value of a '{FEATURES[feature]}' feature type '{feature}'.")
            elif FEATURES[feature] == "Boolean":
                result = self.getBool(feature)
            elif FEATURES[feature] == "Integer":
                result = self.getInt(feature)
            elif FEATURES[feature] == "Floating Point":
                result = self.getFloat(feature)
            elif FEATURES[feature] == "String":
                result = self.getString(feature)
            elif FEATURES[feature] == "Enumerated":
                index = self.getEnumIndex(feature)
                string = self.getEnumStringByIndex(feature, index)
                result = (index, string)
            else:
                # If we get here there's probably a typo in the FEATURES dictionary...
                raise RuntimeError(f"Unknown data type '{FEATURES[feature]}' for the feature '{feature}'.")
        except Exception as ex:
            if errors == "warn":
                log.warn(f"Unable to get value of '{feature}': {ex}")
            elif errors == "raise":
                raise
        return result

    def set_feature(self, feature:str, value, errors="warn"):
        """
        Sets the value of a camera ``feature``, without needing to know the particular data type.

        Internally, calls the appropriate ``setBool``, ``setInt``, ``setFloat``, ``setString`` or ``setEnum`` for ``feature``.
        Enum types may be set using either the index or string representation.

        See :data:`FEATURES` for a list of camera features.

        By default any errors when setting the value are warned about (``errors="warn"``).
        To instead raise exceptions, set ``errors="raise"``.
        To silence errors completely, set ``errors="ignore"``.
        If a value is unable to be set and errors are ignored, ``None`` will be returned.

        :param feature: String matching the camera feature to set.
        :param value: New value of the feature to set.
        :param errors: Action to take on errors, either ``ignore``, ``warn``, or ``raise``.
        """
        try:
            if feature not in FEATURES:
                raise RuntimeError(f"Unknown feature '{feature}'.")
            if FEATURES[feature] == "Command":
                # Setting a command isn't really correct, but we'll allow it (ignoring the given value)
                self.command(feature)
            elif FEATURES[feature] == "Event":
                # Can't set a value for a feature.
                raise RuntimeError(f"Attempted to set the value of a '{FEATURES[feature]}' feature type '{feature}'.")
            elif FEATURES[feature] == "Boolean":
                self.setBool(feature, bool(value))
            elif FEATURES[feature] == "Integer":
                self.setInt(feature, int(value))
            elif FEATURES[feature] == "Floating Point":
                self.setFloat(feature, float(value))
            elif FEATURES[feature] == "String":
                self.setString(feature, str(value))
            elif FEATURES[feature] == "Enumerated":
                if type(value) == int:
                    self.setEnumIndex(feature, value)
                else:
                    self.setEnumString(feature, str(value))
        except Exception as ex:
            if errors == "warn":
                log.warn(f"Unable to set value of '{feature}': {ex}")
            elif errors == "raise":
                raise

    def __getattr__(self, name):
        """
        Intercept ``__getattr__`` calls for class properties which match valid camera features.

        Allows the use of feature names as class properties, for example ``t = cam.ExposureTime``.
        """
        if name in FEATURES:
            return self.get_feature(name)
        else:
            raise AttributeError(f"Attempt to get invalid property '{name}' for Andor3.")

    def __setattr__(self, name, value):
        """
        Intercept __setattr__ calls for class properties which match valid camera features.

        Allows the use of feature names as class properties, for example ``cam.ExposureTime = 0.1``.
        """
        if name in FEATURES:
            self.set_feature(name, value)
        else:
            super().__setattr__(name, value)

    def start(self):
        """
        A shortcut for calling ``cam.command("AcquisitionStart")``.
        """
        error = self.dll.AT_Command(self.camera_handle, "AcquisitionStart")
        if not error == AT_ERR.SUCCESS: raise AndorError(error)
    
    def stop(self):
        """
        A shortcut for calling ``cam.command("AcquisitionStop")``.
        """
        error = self.dll.AT_Command(self.camera_handle, "AcquisitionStop")
        if not error == AT_ERR.SUCCESS: raise AndorError(error)

    def min(self, feature:str, errors="warn"):
        """
        Queries the minimum allowed value of a camera ``feature``, without needing to know the particular data type.

        Internally, calls the appropriate ``getIntMin`` or ``getFloatMin`` for ``feature`` and returns the value.

        See :data:`FEATURES` for a list of camera features.

        By default any errors when querying the value are warned about (``errors="warn"``).
        To instead raise exceptions, set ``errors="raise"``.
        To silence errors completely, set ``errors="ignore"``.
        If a value is unable to be queried and errors are ignored, ``None`` will be returned.

        :param feature: String matching the camera feature to query.
        :param errors: Action to take on errors, either ``ignore``, ``warn``, or ``raise``.
        :returns: Minimum allowed value of the requested feature.
        """
        result = None
        try:
            if feature not in FEATURES:
                raise RuntimeError(f"Unknown feature '{feature}'.")
            if FEATURES[feature] in ("Command", "Event", "Boolean", "String", "Enumerated"):
                # These don't have minimum values.
                raise RuntimeError(f"Attempted to get the minimum of a '{FEATURES[feature]}' feature type '{feature}'.")
            elif FEATURES[feature] == "Integer":
                result = self.getIntMin(feature)
            elif FEATURES[feature] == "Floating Point":
                result = self.getFloatMin(feature)
            else:
                # If we get here there's probably a typo in the FEATURES dictionary...
                raise RuntimeError(f"Unknown data type '{FEATURES[feature]}' for the feature '{feature}'.")
        except Exception as ex:
            if errors == "warn":
                log.warn(f"Unable to get minimum of '{feature}': {ex}")
            elif errors == "raise":
                raise
        return result

    def max(self, feature:str, errors="warn"):
        """
        Queries the maximum allowed value of a camera `feature`, without needing to know the particular data type.

        Internally, calls the appropriate ``getIntMax`` or ``getFloatMax`` for ``feature`` and returns the value.

        See :data:`FEATURES` for a list of camera features.

        By default any errors when querying the value are warned about (``errors="warn"``).
        To instead raise exceptions, set ``errors="raise"``.
        To silence errors completely, set ``errors="ignore"``.
        If a value is unable to be queried and errors are ignored, ``None`` will be returned.

        :param feature: String matching the camera feature to query.
        :param errors: Action to take on errors, either ``ignore``, ``warn``, or ``raise``.
        :returns: Maximum allowed value of the requested feature.
        """
        result = None
        try:
            if feature not in FEATURES:
                raise RuntimeError(f"Unknown feature '{feature}'.")
            if FEATURES[feature] in ("Command", "Event", "Boolean", "String", "Enumerated"):
                # These don't have maximum values.
                raise RuntimeError(f"Attempted to get the maximum of a '{FEATURES[feature]}' feature type '{feature}'.")
            elif FEATURES[feature] == "Integer":
                result = self.getIntMax(feature)
            elif FEATURES[feature] == "Floating Point":
                result = self.getFloatMax(feature)
            else:
                # If we get here there's probably a typo in the FEATURES dictionary...
                raise RuntimeError(f"Unknown data type '{FEATURES[feature]}' for the feature '{feature}'.")
        except Exception as ex:
            if errors == "warn":
                log.warn(f"Unable to get maximum of '{feature}': {ex}")
            elif errors == "raise":
                raise
        return result

    @property
    def features(self):
        """
        A list of feature names available to this camera.
        """
        return [f for f in FEATURES if self.isImplemented(f)]        

    def describe_features(self):
        """
        Generate a string representation of all available camera features and their values.
        """
        s = ""
        for feature, datatype in FEATURES.items():
            if self.isImplemented(feature):
                s += (f"{feature}: "
                    f"{datatype} "
                    f"({'r' if self.isReadable(feature) else '-'}"
                    f"{'w' if self.isWritable(feature) else '-'})\n") 
                if datatype in ("Integer", "Floating Point"):
                    s += (f"  value={self.get_feature(feature):g} "
                        f"min={self.min(feature):g} "
                        f"max={self.max(feature):g}\n")
                elif datatype == "Boolean":
                    s += (f"  value={self.get_feature(feature)}\n")
                elif datatype == "String":
                    s += (f"  value=\"{self.get_feature(feature)}\"\n")
                elif datatype == "Enumerated":
                    for i in range(self.getEnumCount(feature)):
                        if self.isEnumIndexImplemented(feature, i):
                            selected_mark = "->" if self.getEnumIndex(feature) == i else "  "
                            available_mark = ":" if self.isEnumIndexAvailable(feature, i) else "x"
                            s += (f"  {selected_mark} {i:2} {available_mark} {self.getEnumStringByIndex(feature, i)}\n")
        return s.rstrip("\n")

    def decode_image(self, data_raw):

        # Metadata not supported just yet
        if self._image_properties["metadata"]:
            raise NotImplementedError("Image decoding with metadata is not yet supported.")
        
        # Use previously saved image properties
        return decode_image_data(
            data_raw=data_raw,
            encoding=self._image_properties["encoding"],
            width=self._image_properties["width"],
            height=self._image_properties["height"],
            stride=self._image_properties["stride"])


def decode_image_data(data_raw, encoding, width, height, stride):
    """
    Decode raw bytes into an image.

    The decoding process needs to know the ``encoding`` of the data, which should be one of
    ``"Mono12"``, ``"Mono16"``, ``"Mono12Packed"``, or ``"Mono32"``.

    The ``height`` and ``width`` parameters determine the shape of the returned image data in pixels.
    There may be redundant padding bytes at the end of rows of pixels, in which case the ``stride``
    parameter (in bytes) may be larger than expected given the width and bit-depth of the image.

    :param data_raw: Raw image byte data.
    :param encoding: String describing the image encoding method.
    :param width: Width of the resulting image, in pixels.
    :param height: Height of the resulting image, in pixels.
    :param stride: Number of bytes used to encode a single row of pixels.
    """
    # Expect data_raw to always be uint8 direct from waitBuffer calls.
    if not data_raw.dtype == np.uint8:
        raise RuntimeError("Image decoding requires data_raw to be array of uint8 data type.")

    # Metadata can be detected if data size doesn't match that expected by stride*height
    if not data_raw.size == stride*height:
        # Assume extra data is metadata, trim it off
        log.warn("Size of data_raw doesn't match image dimensions (metadata is not yet supported).")
        data_raw = data_raw[0:stride*height]

    # Convert to correct data type, convert stride from bytes to array elements
    if encoding in ("Mono12", "Mono16"):
        # Interpret data as uint16 type (no copy)
        data = data_raw.view(dtype=np.uint16)
        stride = stride//2
    elif encoding == "Mono12Packed":
        # Unpack Mono12Packed into uint16 type (data copy required)
        data = unpack_uint12(data_raw)
        # Stride so should be 1.5x larger now
        stride = 3*stride//2
    elif encoding == "Mono32":
        # Interpret data as uint32 type (no copy)
        data = data_raw.view(dtype=np.uint32)
        stride = stride//4
    else:
        raise RuntimeError(f"Pixel encoding type '{encoding}' not supported, (must be Mono12, Mono12Packed, or Mono32).")
    
    # Reshape from 1D to a 2D array, will still include padding
    data = data.reshape((stride, height), order="F")
    # Slice data array to remove any padding pixels at end of rows
    data = data[0:width,:]

    return data


# TODO: Convenience methods for buffer/image handling.


# numpy routines for data processing, which will be used if the numba library is not available.
# These are generally slower than the numba compiled versions, but not too slow to use.
def np_unpack_uint12(packed_data):
    """
    Unpacks the 12BitPacked image format into an array of unsigned 16-bit integers.

    `packed_data` is numpy array of ``np.uint8``, consisting of pairs of 12-bit numbers packed into 3 byte sequences.

    This routine is written using numpy array operations, which is only about 5x slower than the compiled numba version.
    This method generally shouldn't be called directly.
    Instead, use :meth:`unpack_uint12` which will select the numba or numpy versions as appropriate.

    :param packed_data: Numpy array of ``np.uint8`` containing 12BitPacked image data.
    :returns: Image data as a numpy array of ``np.uint16``.
    """

    # packed_data must be at least two values packed into 3 bytes
    if not packed_data.shape[0]%3 == 0:
        raise RuntimeError("Input data size must be a multiple of 3 bytes (pairs of 12-bit numbers packed into 3 bytes)")

    # Output array, 16-bit unsigned integers. Upper 4 bits will be zero.
    out = np.empty(2*(packed_data.shape[0]//3), dtype=np.uint16)

    # This looks simple but uses extra temporary data structures
    #out[0::2] = (packed_data[0::3].astype(np.uint16) << 4) + (packed_data[1::3].astype(np.uint16) & 0xF)
    #out[1::2] = (packed_data[2::3].astype(np.uint16) << 4) + (packed_data[1::3].astype(np.uint16) >> 4)

    # This looks uglier, but is 30% faster
    out[0::2] = packed_data[0::3]
    out[0::2] = out[0::2] << 4
    out[0::2] += packed_data[1::3] & 0xF

    out[1::2] = packed_data[2::3]
    out[1::2] = out[1::2] << 4
    out[1::2] += packed_data[1::3] >> 4

    return out
# Use numpy version by default
unpack_uint12 = np_unpack_uint12


def np_fvb(image):
    """
        Perform full-vertical-binning (FVB) of image data.

        ``image`` is a 2-dimensional numpy array of image data, where the first dimension indexes the
        column (width, x-coordinate) of the image, the second the row (height, y-coordinate).
        
        The vertically binned data will be returned as the mean as a 1-dimensional array of float32.

        This numpy routine simply takes the mean across the second axis and is fast, but only single-threaded.
        The numba version is faster due to parallelisation.
        This method generally shouldn't be called directly.
        Instead, use :meth:`fvb` which will select the numba or numpy versions as appropriate.


        :param image: Numpy array of image data.
        :returns: Vertically binned array of ``np.float32``.
        """
    return np.mean(image, axis=1).astype(np.float32)
# Use numpy version by default
fvb = np_fvb


# Use numba accelerated routines if available
try:
    import numba as nb
    
    @nb.njit(nb.uint16[::1](nb.uint8[::1]), fastmath=True, parallel=True)
    def nb_unpack_uint12(packed_data):
        """
        Unpacks the 12BitPacked image format into an array of unsigned 16-bit integers.

        `packed_data` is numpy array of ``np.uint8``, consisting of pairs of 12-bit numbers packed into 3 byte sequences.

        This routine is written in a very simplistic manner which the numba just-in-time (JIT) compiler is easily able to optimize.
        Running this as pure python code is not advisable! Tests indicate it is about 6500x slower than the compiled version.
        In case the numba library is unavailable, a numpy routine will be used instead, which is only about 5x slower.
        This method generally shouldn't be called directly.
        Instead, use :meth:`unpack_uint12` which will select the numba or numpy versions as appropriate.

        :param packed_data: Numpy array of ``np.uint8`` containing 12BitPacked image data.
        :returns: Image data as a numpy array of ``np.uint16``.
        """
        # packed_data must be at least two values packed into 3 bytes
        if not packed_data.shape[0]%3 == 0:
            raise RuntimeError("Input data size must be a multiple of 3 bytes (pairs of 12-bit numbers packed into 3 bytes)")

        # Output array, 16-bit unsigned integers. Upper 4 bits will be zero.
        out = np.empty(2*(packed_data.shape[0]//3), dtype=np.uint16)

        for i in nb.prange(packed_data.shape[0]//3):
            byte1 = np.uint16(packed_data[i*3])
            byte2 = np.uint16(packed_data[i*3 + 1])
            byte3 = np.uint16(packed_data[i*3 + 2])
            out[2*i]     = (byte1 << 4) + (byte2 & 0xF)
            out[2*i + 1] = (byte3 << 4) + (byte2 >> 4)

        return out
    # Override with numba version
    unpack_uint12 = nb_unpack_uint12


    @nb.njit([nb.float32[:](nb.uint16[:,:]), nb.float32[:](nb.uint32[:,:])], parallel=True)
    def nb_fvb(image):
        """
        Perform full-vertical-binning (FVB) of image data.

        ``image`` is a 2-dimensional numpy array of image data in uint16 or uint32 format, where the
        first dimension indexes the column (width, x-coordinate) of the image, the second the row (height, y-coordinate).
        
        The vertically binned data will be returned as the mean as a 1-dimensional array of float32.

        This numba accelerated routine is not intrinsically faster than the numpy version on a single CPU core,
        but is faster because of parallelisation.
        This method generally shouldn't be called directly.
        Instead, use :meth:`fvb` which will select the numba or numpy versions as appropriate.

        :param image: Numpy array of image data in uint16 or uint32 format.
        :returns: Vertically binned array of ``np.float32``.
        """
        result = np.zeros((image.shape[0],), dtype=np.uint64)
        for col in nb.prange(image.shape[0]):
            for row in nb.prange(image.shape[1]):
                result[col] += image[col,row]
        return (result/image.shape[1]).astype(np.float32)
    # Override with numba version
    fvb = nb_fvb


except:
    log.warn("The numba library is not available. Pure numpy routines will be used instead but performance may suffer.")


class AndorError(RuntimeError):
    """
    Exception used to indicate an error returned by the Andor SDK3.

    :param error_code: Numerical error code used by the Andor SDK3.
    """

    def __init__(self, error_code):
        self.error_code = error_code
    
    def __str__(self):
        return f"AT_ERR_{AT_ERR(self.error_code).name} ({self.error_code}): {AT_ERR(self.error_code).description}"


class AT_ERR(IntEnum):
    """
    Enumeration listing the valid Andor SDK3 numerical error codes.
    """
    SUCCESS = 0
    NOTINITIALISED = 1
    NOTIMPLEMENTED = 2
    READONLY = 3
    NOTREADABLE = 4
    NOTWRITABLE = 5
    OUTOFRANGE = 6
    INDEXNOTAVAILABLE = 7
    INDEXNOTIMPLEMENTED = 8
    EXCEEDEDMAXSTRINGLENGTH = 9
    CONNECTION = 10
    NODATA = 11
    INVALIDHANDLE = 12
    TIMEDOUT = 13
    BUFFERFULL = 14
    INVALIDSIZE = 15
    INVALIDALIGNMENT = 16
    COMM = 17
    STRINGNOTAVAILABLE = 18
    STRINGNOTIMPLEMENTED = 19
    NULL_FEATURE = 20
    NULL_HANDLE = 21
    NULL_IMPLEMENTED_VAR = 22
    NULL_READABLE_VAR = 23
    NULL_READONLY_VAR = 24
    NULL_WRITABLE_VAR = 25
    NULL_MINVALUE = 26
    NULL_MAXVALUE = 27
    NULL_VALUE = 28
    NULL_STRING = 29
    NULL_COUNT_VAR = 30
    NULL_ISAVAILABLE_VAR = 31
    NULL_MAXSTRINGLENGTH = 32
    NULL_EVCALLBACK = 33
    NULL_QUEUE_PTR = 34
    NULL_WAIT_PTR = 35
    NULL_PTRSIZE = 36
    NOMEMORY = 37
    DEVICEINUSE = 38
    DEVICENOTFOUND = 39
    HARDWARE_OVERFLOW = 100

    @property
    def description(self):
        """
        Return a string describing the error code.
        """
        return {
            AT_ERR.SUCCESS : "Function call was successful",
            AT_ERR.NOTINITIALISED : "Function called with an uninitialized handle",
            AT_ERR.NOTIMPLEMENTED : "Feature has not been implemented for the chosen camera",
            AT_ERR.READONLY : "Feature is read only",
            AT_ERR.NOTREADABLE : "Feature is currently not readable",
            AT_ERR.NOTWRITABLE : "Feature is currently not writable",
            AT_ERR.OUTOFRANGE : "Value is outside the maximum and minimum limits",
            AT_ERR.INDEXNOTAVAILABLE : "Index is currently not available",
            AT_ERR.INDEXNOTIMPLEMENTED : "Index is not implemented for the chosen camera",
            AT_ERR.EXCEEDEDMAXSTRINGLENGTH : "String value provided exceeds the maximum allowed length",
            AT_ERR.CONNECTION : "Error connecting to or disconnecting from hardware",
            AT_ERR.NODATA : "No Internal Event or Internal Error",
            AT_ERR.INVALIDHANDLE : "Invalid device handle passed to function",
            AT_ERR.TIMEDOUT : "The waitBuffer function timed out while waiting for data arrive in output queue",
            AT_ERR.BUFFERFULL : "The input queue has reached its capacity",
            AT_ERR.INVALIDSIZE : "The size of a queued buffer did not match the frame size",
            AT_ERR.INVALIDALIGNMENT : "A queued buffer was not aligned on an 8-byte boundary",
            AT_ERR.COMM : "An error has occurred while communicating with hardware",
            AT_ERR.STRINGNOTAVAILABLE : "Index / String is not available",
            AT_ERR.STRINGNOTIMPLEMENTED : "Index / String is not implemented for the chosen camera",
            AT_ERR.NULL_FEATURE : "NULL feature name passed to function",
            AT_ERR.NULL_HANDLE : "Null device handle passed to function",
            AT_ERR.NULL_IMPLEMENTED_VAR : "Feature not implemented",
            AT_ERR.NULL_READABLE_VAR : "Readable not set",
            AT_ERR.NULL_READONLY_VAR : "Read-only",
            AT_ERR.NULL_WRITABLE_VAR : "Writable not set",
            AT_ERR.NULL_MINVALUE : "NULL min value",
            AT_ERR.NULL_MAXVALUE : "NULL max value",
            AT_ERR.NULL_VALUE : "NULL value returned from function",
            AT_ERR.NULL_STRING : "NULL string returned from function",
            AT_ERR.NULL_COUNT_VAR : "NULL feature count",
            AT_ERR.NULL_ISAVAILABLE_VAR : "Available not set",
            AT_ERR.NULL_MAXSTRINGLENGTH : "Max string length is NULL",
            AT_ERR.NULL_EVCALLBACK : "EvCallBack parameter is NULL",
            AT_ERR.NULL_QUEUE_PTR : "Pointer to queue is NULL",
            AT_ERR.NULL_WAIT_PTR : "Wait pointer is NULL",
            AT_ERR.NULL_PTRSIZE : "Pointer size is NULL",
            AT_ERR.NOMEMORY : "No memory has been allocated for the current action",
            AT_ERR.DEVICEINUSE : "Function failed to connect to a device because it is already being used",
            AT_ERR.DEVICENOTFOUND : "Device not found",
            AT_ERR.HARDWARE_OVERFLOW : "The software was not able to retrieve data from the card or camera fast enough to avoid the internal hardware buffer bursting."
        }[self.value]


class AT_HANDLE(IntEnum):
    """
    Enumeration of special camera handle values used by the Andor SDK3.
    """
    UNINITIALISED = -1
    SYSTEM = 1