//
//  ViewController.swift
//  SwiftCodeMetricsExample
//
//  Created by Mattia Campolese on 05/08/2018.
//  Copyright © 2018 Mattia Campolese. All rights reserved.
//

import UIKit
import BusinessLogic

class ViewController: UIViewController {

    @IBAction func btnLaunchAwesomeAction(_ sender: Any) {
        launchFeature(with: true)
    }
    
    @IBAction func btnLaunchNotSoAwesomeAction(_ sender: Any) {
        launchFeature(with: false)
    }
    
    private func launchFeature(with awesomeness: Bool) {
        let viewController: UIViewController = awesomeness ? AwesomeFeatureViewController() : NotSoAwesomeFeatureViewController()
        navigationController?.pushViewController(viewController, animated: true)
    }
    
}

