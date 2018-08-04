//
//  ExampleFile.swift
//  
//
//  Created by Mattia Campolese on 06/07/2018.
//

import Foundation
import AmazingFramework

// First protocol SimpleProtocol
protocol SimpleProtocol {}

// First class SimpleClass
class SimpleClass: SimpleProtocol {
    
    func methodOne() {
        // Some implementation
    }
    
    func methodTwo(with param1: Int, param2: Int) -> Int {
        return param1 + param2
    }
    
    private func privateFunction() {}
    
}

// Second class ComplexClass
final class ComplexClass: SimpleClass {
    
    /*
     This should contain more important code
     protocol test
     class shouldNotBeRecognized
    */
    
    static func aStaticMethod() {
        
    }
    
}

// Third element, struct
struct GenericStruct<T> {
    
}

// Fourth class
public final class ComposedAttributedClass {}

// Fifth class
final fileprivate class ComposedPrivateClass {}

// Sixth element, struct
internal struct InternalStruct {
    
}

/* yet another comment, this time is in-line - total 20 lines of comments here */
