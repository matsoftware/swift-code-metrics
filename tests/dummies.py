from swift_code_metrics._metrics import Framework


def dummy_external_frameworks():
    return [
        Framework('Foundation'),
        Framework('UIKit'),
        Framework('RxSwift'),
    ]