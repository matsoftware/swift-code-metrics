//
//  ExampleFile.swift
//  
//
//  Created by Mattia Campolese on 06/07/2018.
//

import Foundation
import AmazingFramework

protocol SimpleProtocol {}

class SimpleClass: SimpleProtocol {
    
    func methodOne() {
        // Some implementation
    }
    
    func methodTwo(with param1: Int, param2: Int) -> Int {
        return param1 + param2
    }
    
}

final class ComplexClass: SimpleClass {
    
    /*
     This should contain more important code
    */
    
    static func aStaticMethod() {
        
    }
    
}
