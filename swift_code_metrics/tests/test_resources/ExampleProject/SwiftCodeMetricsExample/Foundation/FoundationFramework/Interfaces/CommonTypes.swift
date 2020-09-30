//
//  CommonTypes.swift
//  FoundationFramework
//
//  Created by Mattia Campolese on 29/09/2020.
//  Copyright © 2020 Mattia Campolese. All rights reserved.
//

import Foundation

public enum Result {

    case success(data: Data)
    case error(error: Error)

}

public enum NetworkingError: Error, Equatable {
    case dummyError
}

public typealias ResultHandler = (Result) -> Void

public protocol NetworkingProtocol {

    func makeRequest(with dummyUrl: URL, result: ResultHandler)

}
