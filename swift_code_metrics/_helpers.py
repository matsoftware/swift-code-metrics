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
        'AccessoryAccess',
        'AccessoryLiveActivities',
        'AccessoryNotifications',
        'AccessorySetupKit',
        'AccessoryTransportExtension',
        'Accounts',
        'ActivityKit',
        'AdAttributionKit',
        'AddressBook',
        'AddressBookUI',
        'AdServices',
        'AdSupport',
        'AGL',
        'AlarmKit',
        'Algorithms',
        'AppClip',
        'AppIntents',
        'AppIntentsTypeSupport',
        'AppKit',
        'AppleArchive',
        'AppleScriptKit',
        'AppleScriptObjC',
        'AppleTextureEncoder',
        'ApplicationServices',
        'AppManagedFeatures',
        'AppMigrationKit',
        'AppTrackingTransparency',
        'ArgumentParser',
        'ARKit',
        'AssetsLibrary',
        'Assignables',
        'Atomics',
        'AudioAccessoryKit',
        'AudioToolbox',
        'AudioUnit',
        'AudioVideoBridging',
        'AuthenticationServices',
        'AutomatedDeviceEnrollment',
        'AutomaticAssessmentConfiguration',
        'Automator',
        'AVFAudio',
        'AVFoundation',
        'AVKit',
        'AVRouting',
        'AVSystemRouting',
        'BackgroundAssets',
        'BackgroundTasks',
        'BrowserEngineCore',
        'BrowserEngineKit',
        'BrowserKit',
        'BusinessChat',
        'CalendarStore',
        'CallKit',
        'Carbon',
        'CarKey',
        'CarPlay',
        'CFNetwork',
        'Charts',
        'Cinematic',
        'ClassKit',
        'ClassKitUI',
        'ClockKit',
        'CloudKit',
        'Cocoa',
        'Collaboration',
        'ColorSync',
        'Combine',
        'CompositorServices',
        'Compression',
        'ComputeGraph',
        'ContactProvider',
        'Contacts',
        'ContactsUI',
        'CoreAI',
        'CoreAnimation',
        'CoreAudio',
        'CoreAudioKit',
        'CoreAudioTypes',
        'CoreBluetooth',
        'CoreData',
        'CoreDisplay',
        'CoreFoundation',
        'CoreGraphics',
        'CoreHaptics',
        'CoreHID',
        'CoreImage',
        'CoreLocation',
        'CoreLocationUI',
        'CoreMedia',
        'CoreMediaIO',
        'CoreMIDI',
        'CoreMIDIServer',
        'CoreML',
        'CoreMotion',
        'CoreNFC',
        'CoreServices',
        'CoreSpotlight',
        'CoreTelephony',
        'CoreText',
        'CoreTransferable',
        'CoreVideo',
        'CoreWLAN',
        'CrashReportExtension',
        'CreateML',
        'CreateMLComponents',
        'CryptoKit',
        'CryptoTokenKit',
        'Darwin',
        'DarwinNotify',
        'DataDetection',
        'DeclaredAgeRange',
        'DeveloperToolsSupport',
        'DeviceActivity',
        'DeviceCheck',
        'DeviceDiscoveryExtension',
        'DeviceDiscoveryUI',
        'DirectoryService',
        'DiscRecording',
        'DiscRecordingUI',
        'DiskArbitration',
        'DiskImageKit',
        'Dispatch',
        'Distributed',
        'dnssd',
        'DockKit',
        'DriverKit',
        'DVDPlayback',
        'EndpointSecurity',
        'EnergyKit',
        'EventKit',
        'EventKitUI',
        'ExceptionHandling',
        'ExecutionPolicy',
        'ExposureNotification',
        'ExtensionFoundation',
        'ExtensionKit',
        'ExternalAccessory',
        'FamilyControls',
        'FileProvider',
        'FileProviderUI',
        'FinanceKit',
        'FinanceKitUI',
        'FinderSync',
        'ForceFeedback',
        'Foundation',
        'FoundationModels',
        'FoveatedStreaming',
        'FSKit',
        'FWAUserLib',
        'FxPlug',
        'GameController',
        'GameKit',
        'GameplayKit',
        'GameSave',
        'GenerateManual',
        'GeoToolbox',
        'GLKit',
        'GLUT',
        'GroupActivities',
        'GSS',
        'HealthKit',
        'HealthKitUI',
        'HIDDriverKit',
        'HomeExtensions',
        'HomeKit',
        'HTTPLiveStreaming',
        'Hypervisor',
        'iAd',
        'ICADevices',
        'IdentityDocumentServices',
        'IdentityDocumentServicesUI',
        'IdentityLookup',
        'IdentityLookupUI',
        'ImageCaptureCore',
        'ImageIO',
        'ImagePlayground',
        'ImmersiveMediaSupport',
        'InputMethodKit',
        'InstallerPlugins',
        'InstantMessage',
        'Intents',
        'IntentsUI',
        'IOBluetooth',
        'IOBluetoothUI',
        'IOKit',
        'IOSurface',
        'IOUSBHost',
        'iTunesLibrary',
        'JavaScriptCore',
        'JournalingSuggestions',
        'Kerberos',
        'Kernel',
        'KernelManagement',
        'LatentSemanticMapping',
        'LDAP',
        'LightweightCodeRequirements',
        'LinkPresentation',
        'LinkSecurity',
        'LiveCommunicationKit',
        'LocalAuthentication',
        'LocalAuthenticationEmbeddedUI',
        'LockedCameraCapture',
        'Logging',
        'MailKit',
        'ManagedApp',
        'ManagedAppDistribution',
        'ManagedSettings',
        'ManagedSettingsUI',
        'MapKit',
        'MarketplaceKit',
        'Matter',
        'MatterSupport',
        'MediaAccessibility',
        'MediaDevice',
        'MediaExtension',
        'MediaIntelligence',
        'MediaIntents',
        'MediaLibrary',
        'MediaPlayer',
        'MediaSetup',
        'MediaToolbox',
        'Messages',
        'MessageUI',
        'Metal',
        'MetalFX',
        'MetalKit',
        'MetalPerformancePrimitives',
        'MetalPerformanceShaders',
        'MetalPerformanceShadersGraph',
        'MetricKit',
        'MLCompute',
        'MobileCoreServices',
        'ModelIO',
        'MultipeerConnectivity',
        'MusicKit',
        'MusicUnderstanding',
        'NaturalLanguage',
        'NearbyInteraction',
        'NetFS',
        'Network',
        'networkext',
        'NetworkExtension',
        'NetworkingDriverKit',
        'NewsstandKit',
        'NotificationCenter',
        'NowPlaying',
        'ObjectiveC',
        'Observation',
        'OpenAL',
        'OpenCL',
        'OpenDirectory',
        'OpenGL',
        'OpenGLES',
        'os',
        'os_object',
        'OSAKit',
        'OSLog',
        'PaperKit',
        'ParavirtualizedGraphics',
        'PassKit',
        'PCSC',
        'PDFKit',
        'PencilKit',
        'PermissionKit',
        'PHASE',
        'PhotoKit',
        'Photos',
        'PhotosUI',
        'PreferencePanes',
        'ProximityReader',
        'PushKit',
        'PushToTalk',
        'QTKit',
        'Quartz',
        'QuartzCore',
        'QuickLook',
        'QuickLookThumbnailing',
        'QuickLookUI',
        'RealityFoundation',
        'RealityKit',
        'RegexBuilder',
        'RelevanceKit',
        'ReplayKit',
        'RoomPlan',
        'SafariServices',
        'SafetyKit',
        'SceneKit',
        'ScreenCaptureKit',
        'ScreenSaver',
        'ScreenTime',
        'ScriptingBridge',
        'SecureElementCredential',
        'Security',
        'SecurityFoundation',
        'SecurityInterface',
        'SecurityUI',
        'SensitiveContentAnalysis',
        'SensorKit',
        'ServiceManagement',
        'ServicesAccountLinking',
        'SharedWithYou',
        'SharedWithYouCore',
        'ShazamKit',
        'simd',
        'SiriKit',
        'SMS',
        'Social',
        'SoundAnalysis',
        'Spatial',
        'SpatialPreview',
        'Speech',
        'SpriteKit',
        'StateReporting',
        'StickerFoundation',
        'StickerKit',
        'StoreKit',
        'StoreKitTest',
        'SuggestedActions',
        'Swift',
        'SwiftData',
        'SwiftUI',
        'SwiftUICore',
        'Symbols',
        'Synchronization',
        'SyncServices',
        'System',
        'SystemConfiguration',
        'SystemExtensions',
        'TabletopKit',
        'TabularData',
        'TelephonyMessagingKit',
        'Testing',
        'ThreadNetwork',
        'TipKit',
        'TouchController',
        'Translation',
        'TranslationUIProvider',
        'TrustInsights',
        'TVML',
        'TVMLKit',
        'TVMLKit JS',
        'TVServices',
        'TVUIKit',
        'TWAIN',
        'UIKit',
        'UniformTypeIdentifiers',
        'USBDriverKit',
        'USDKit',
        'UserNotifications',
        'UserNotificationsUI',
        'vecLib',
        'VideoDecodeAcceleration',
        'VideoSubscriberAccount',
        'VideoToolbox',
        'Virtualization',
        'Vision',
        'VisionEntitlementServices',
        'VisionKit',
        'VisualIntelligence',
        'vmnet',
        'WatchConnectivity',
        'WatchKit',
        'WeatherKit',
        'WebKit',
        'WidgetKit',
        'WiFiAware',
        'WiFiInfrastructure',
        'WirelessInsights',
        'WorkoutKit',
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
