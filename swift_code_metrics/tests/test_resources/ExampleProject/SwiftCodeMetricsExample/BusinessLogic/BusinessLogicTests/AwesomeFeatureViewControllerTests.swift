//
//  AwesomeFeatureViewControllerTests.swift
//  BusinessLogicTests
//
//  Created by Mattia Campolese on 05/08/2018.
//  Copyright © 2018 Mattia Campolese. All rights reserved.
//

import XCTest
@testable import BusinessLogic

class AwesomeFeatureViewControllerTests: XCTestCase {
    
    func test_awesomeFeatureViewController_baseRequestPath() {
        
        XCTAssertEqual(AwesomeFeatureViewController().baseRequestPath, "/such/an/awesome/app")
    
    }
    
}
