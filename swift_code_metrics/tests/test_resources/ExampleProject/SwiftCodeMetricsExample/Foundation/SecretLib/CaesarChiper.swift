//
//  CaesarChiper.swift
//  SecretLib
//
//  Created by Mattia Campolese on 26/02/2019.
//  Copyright © 2019 Mattia Campolese. All rights reserved.
//

import Foundation

public struct CaesarChiper {
    
    public static func encrypt(message: String, shift: Int) -> String {
        
        let scalars = Array(message.unicodeScalars)
        let unicodePoints = scalars.map({x in Character(UnicodeScalar(Int(x.value) + shift)!)})
        
        return String(unicodePoints)
    }
    
}
