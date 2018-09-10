//
//  AwesomeFeature.swift
//  BusinessLogic
//
//  Created by Mattia Campolese on 05/08/2018.
//  Copyright © 2018 Mattia Campolese. All rights reserved.
//

import UIKit
import FoundationFramework

public class FeatureViewController: UIViewController {
    
    var label: UILabel!
    var baseRequestPath: String {
        assertionFailure("Should override in subclass")
        return ""
    }
    
    override public func loadView() {
        super.loadView()
        label = UILabel()
        label.translatesAutoresizingMaskIntoConstraints = false
        label.textAlignment = .center
        view.addSubview(label)
        NSLayoutConstraint.activate([
            label.topAnchor.constraint(equalTo: view.topAnchor),
            label.bottomAnchor.constraint(equalTo: view.bottomAnchor),
            label.leadingAnchor.constraint(equalTo: view.leadingAnchor),
            label.trailingAnchor.constraint(equalTo: view.trailingAnchor),
            ])
    }
    
    override public func viewDidLoad() {
        super.viewDidLoad()
        fetchData()
    }
    
    func fetchData() {
        let client = Networking()
        client.makeRequest(with: URL(fileURLWithPath: baseRequestPath)) { res in
            switch res {
            case .success(data: let data):
                label.text = String(data: data, encoding: .utf8)
                view.backgroundColor = .green
            case .error(error: let error):
                view.backgroundColor = .red
                label.text = error.localizedDescription
            }
        }
    }
    
}

public final class AwesomeFeatureViewController: FeatureViewController {
    
    override var baseRequestPath: String {
        return "/such/an/awesome/app"
    }
    
}


public final class NotSoAwesomeFeatureViewController: FeatureViewController {
    
    override var baseRequestPath: String {
        return "/not/an/awesome/error"
    }
    
}

