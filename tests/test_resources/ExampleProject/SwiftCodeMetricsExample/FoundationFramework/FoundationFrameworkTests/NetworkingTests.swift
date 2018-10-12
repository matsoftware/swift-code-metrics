//
//  NetworkingTests.swift
//  FoundationFrameworkTests
//
//  Created by Mattia Campolese on 12/10/2018.
//  Copyright © 2018 Mattia Campolese. All rights reserved.
//

import Foundation
import XCTest
@testable import FoundationFramework

final class NetworkingTests: XCTestCase {
    
    var networking: Networking!
    
    override func setUp() {
        super.setUp()
        networking = Networking()
    }
    
    override func tearDown() {
        networking = nil
        super.tearDown()
    }
    
    func test_networking_makeRequest_dummyUrlError_shouldFail() {
        
        var called = 0
        networking.makeRequest(with: URL(string: "http://any.error")!) { res in
            called += 1
            guard case .error(NetworkingError.dummyError) = res else {
                XCTFail("Not an error")
                return
            }
        }
        
        XCTAssertEqual(called, 1)
        
    }
 
    func test_networking_makeRequest_anyOtherUrl_shouldSucceed() {
        
        var called = 0
        networking.makeRequest(with: URL(string: "http://any.other.url")!) { res in
            called += 1
            guard case .success = res else {
                XCTFail("Not a success")
                return
            }
        }
        
        XCTAssertEqual(called, 1)
        
    }
    
}
