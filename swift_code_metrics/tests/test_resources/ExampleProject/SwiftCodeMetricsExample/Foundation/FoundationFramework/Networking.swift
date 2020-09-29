//
//  Networking.swift
//  FoundationFramework
//
//  Created by Mattia Campolese on 05/08/2018.
//  Copyright © 2018 Mattia Campolese. All rights reserved.
//

import Foundation

public struct Networking: NetworkingProtocol {
    
    public init() {}
    
    public func makeRequest(with dummyUrl: URL, result: ResultHandler) {
        if dummyUrl.absoluteString.hasSuffix("error") {
            result(.error(error: NetworkingError.dummyError))
        } else {
            result(.success(data: "Success".data(using: .utf8)!))
        }
    }
    
}
