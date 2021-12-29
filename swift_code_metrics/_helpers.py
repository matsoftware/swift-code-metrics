import re
import logging
import json
from typing import Dict
from functional import seq


class Log:
    __logger = logging.getLogger(__name__)

    @classmethod
    def warn(cls, message: str):
        Log.__logger.warning(message)


class AnalyzerHelpers:
    # Constants

    SWIFT_FILE_EXTENSION = '.swift'

    # List of frameworks owned by Apple™️ that are excluded from the analysis.
    # This list is manually updated and references the content available from
    # https://developer.apple.com/documentation/technologies?changes=latest_major,
    # https://developer.apple.com/ios/whats-new/ and https://developer.apple.com/macos/whats-new/
    APPLE_FRAMEWORKS = [
        'Accelerate',
        'Accessibility',
        'Accounts',
        'AddressBook',
        'AddressBookUI',
        'AdSupport',
        'AGL',
        'AppClip',
        'AppKit',
        'AppleArchive',
        'ApplicationServices',
        'AppTrackingTransparency',
        'ARKit',
        'AssetsLibrary',
        'AudioToolbox',
        'AudioUnit',
        'AuthenticationServices',
        'AutomaticAssessmentConfiguration',
        'AVFoundation',
        'AVKit',
        'BackgroundTasks',
        'CallKit',
        'CarPlay',
        'CFNetwork',
        'ClassKit',
        'ClockKit',
        'CloudKit',
        'Collaboration',
        'ColorSync',
        'Combine',
        'Compression',
        'Contacts',
        'ContactsUI',
        'CoreAnimation',
        'CoreAudio',
        'CoreAudioKit',
        'CoreAudioTypes',
        'CoreBluetooth',
        'CoreData',
        'CoreFoundation',
        'CoreGraphics',
        'CoreHaptics',
        'CoreImage',
        'CoreLocation',
        'CoreLocationUI',
        'CoreMedia',
        'CoreMIDI',
        'CoreML',
        'CoreMotion',
        'CoreNFC',
        'CoreServices',
        'CoreSpotlight',
        'CoreTelephony',
        'CoreText',
        'CoreVideo',
        'CoreWLAN',
        'CreateML',
        'CryptoKit',
        'CryptoTokenKit',
        'DarwinNotify',
        'DeveloperToolsSupport',
        'DeviceActivity',
        'DeviceCheck',
        'DiskArbitration',
        'Dispatch',
        'dnssd',
        'DriverKit',
        'EndpointSecurity',
        'EventKit',
        'EventKitUI',
        'ExceptionHandling',
        'ExecutionPolicy',
        'ExposureNotification',
        'ExternalAccessory',
        'FamilyControls',
        'FileProvider',
        'FileProviderUI',
        'FinderSync',
        'ForceFeedback',
        'Foundation',
        'FWAUserLib',
        'FxPlug',
        'GameController',
        'GameKit',
        'GameplayKit',
        'GLKit',
        'GroupActivities',
        'GSS',
        'HealthKit',
        'HIDDriverKit',
        'HomeKit',
        'HTTPLiveStreaming',
        'Hypervisor',
        'iAd',
        'InputMethodKit',
        'IOBluetooth',
        'IOBluetoothUI',
        'IOKit',
        'IOSurface',
        'IOUSBHost',
        'iTunesLibrary',
        'JavaScriptCore',
        'Kernel',
        'KernelManagement',
        'LatentSemanticMapping',
        'LinkPresentation',
        'LocalAuthentication',
        'Logging',
        'ManagedSettings',
        'ManagedSettingsUI',
        'MapKit',
        'MediaAccessibility',
        'MediaLibrary',
        'MediaPlayer',
        'MediaSetup',
        'Messages',
        'MessageUI',
        'MetalKit',
        'MetricKit',
        'MobileCoreServices',
        'MultipeerConnectivity',
        'MusicKit',
        'NaturalLanguage',
        'NearbyInteraction',
        'Network',
        'NetworkExtension',
        'NetworkingDriverKit',
        'NewsstandKit',
        'NotificationCenter',
        'ObjectiveC',
        'OpenDirectory',
        'OpenGL',
        'os',
        'ParavirtualizedGraphics',
        'PassKit',
        'PDFKit',
        'PencilKit',
        'PhotoKit',
        'PushKit',
        'QTKit',
        'QuartzCore',
        'QuickLook',
        'QuickLookThumbnailing',
        'RealityKit',
        'ReplayKit',
        'SafariServices',
        'SceneKit',
        'ScreenSaver',
        'ScreenTime',
        'Security',
        'SecurityFoundation',
        'SecurityInterface',
        'SensorKit',
        'ServiceManagement',
        'ShazamKit',
        'simd',
        'SiriKit',
        'SMS',
        'Social',
        'SoundAnalysis',
        'Speech',
        'SpriteKit',
        'StoreKit',
        'StoreKitTest',
        'SwiftUI',
        'System',
        'SystemConfiguration',
        'SystemExtensions',
        'TVML',
        'TVMLKit JS',
        'TVMLKit',
        'TVServices',
        'TVUIKit',
        'UIKit',
        'UniformTypeIdentifiers',
        'USBDriverKit',
        'UserNotifications',
        'UserNotificationsUI',
        'VideoToolbox',
        'Virtualization',
        'Vision',
        'VisionKit',
        'vmnet'
        'WatchConnectivity',
        'WatchKit',
        'WebKit',
        'WidgetKit',
        'XCTest',
        'XPC'
    ]

    @staticmethod
    def is_path_in_list(subdir, exclude_paths):
        for p in exclude_paths:
            if p in subdir:
                return True
        return False


class ParsingHelpers:
    # Constants

    DEFAULT_FRAMEWORK_NAME = 'AppTarget'
    DEFAULT_TEST_FRAMEWORK_SUFFIX = '_Test'
    TEST_METHOD_PREFIX = 'test'
    FRAMEWORK_STRUCTURE_OVERRIDE_FILE = 'scm.json'

    # Constants - Regex patterns

    BEGIN_COMMENT = r'^//*'
    END_COMMENT = r'\*/$'
    SINGLE_COMMENT = r'^//'

    IMPORTS = r'(?:(?<=^import )|@testable import )(?:\b\w+\s|)([^.; \/]+)'

    PROTOCOLS = r'.*protocol (.*?)[:|{|\s]'
    STRUCTS = r'.*struct (.*?)[:|{|\s]'
    CLASSES = r'.*class (.*?)[:|{|\s]'
    FUNCS = r'.*func (.*?)[:|\(|\s]'

    # Static helpers

    @staticmethod
    def check_existence(regex_pattern, trimmed_string):
        regex = re.compile(regex_pattern)
        if re.search(regex, trimmed_string.strip()) is not None:
            return True
        else:
            return False

    @staticmethod
    def extract_substring_with_pattern(regex_pattern, trimmed_string):
        try:
            return re.search(regex_pattern, trimmed_string).group(1)
        except AttributeError:
            return ''

    @staticmethod
    def reduce_dictionary(items: Dict[str, int]) -> int:
        if len(items.values()) == 0:
            return 0
        return seq(items.values()) \
            .reduce(lambda f1, f2: f1 + f2)


class ReportingHelpers:

    @staticmethod
    def decimal_format(number, decimal_places=3):
        format_string = "{:." + str(decimal_places) + "f}"
        return float(format_string.format(number))


class JSONReader:

    @staticmethod
    def read_json_file(path: str) -> Dict:
        with open(path, 'r') as fp:
            return json.load(fp)
