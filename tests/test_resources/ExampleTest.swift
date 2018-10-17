import XCTest

final class ExampleTest: XCTestCase {
    
    func test_example_assertion() {
        XCTAssertEqual(1,1)
    }
    
    func testAnotherExample() {
        mockHelperFunctionInTest()
        XCTAssertEqual(2,2)
    }
    
    private func mockHelperFunctionInTest() {
        
    }
    
}
