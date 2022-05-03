result = {
    "status": "succeeded",
    "createdDateTime": "2022-05-03T17:40:31Z",
    "lastUpdatedDateTime": "2022-05-03T17:40:33Z",
    "analyzeResult": {
        "apiVersion": "2022-01-30-preview",
        "modelId": "prebuilt-idDocument",
        "stringIndexType": "textElements",
        "content": "California\nDRIVER LICENSE\nCLASS C\nDL F89264518\nExp 01/01/2025\nLN Puelma\nFN\nDiogo Andrés\n988 San Martín Ave, Apt B\nConcepción, Chile, 98102\nDOB 01/17/1990\nRSTR\nEND NONE\nDONOR\nSEX: M\nHGT\nD\nHAIR BRN\nWGT\nEYES BLK\nISS\n08/08/2020",
        "pages": [
            {
                "pageNumber": 1,
                "angle": 0,
                "width": 507,
                "height": 310,
                "unit": "pixel",
                "words": [
                    {
                        "content": "California",
                        "boundingBox": [28, 6, 193, 7, 192, 40, 27, 41],
                        "confidence": 0.993,
                        "span": {"offset": 0, "length": 10},
                    },
                    {
                        "content": "DRIVER",
                        "boundingBox": [240, 12, 297, 12, 298, 27, 241, 28],
                        "confidence": 0.999,
                        "span": {"offset": 11, "length": 6},
                    },
                    {
                        "content": "LICENSE",
                        "boundingBox": [305, 12, 375, 12, 375, 27, 305, 27],
                        "confidence": 0.994,
                        "span": {"offset": 18, "length": 7},
                    },
                    {
                        "content": "CLASS",
                        "boundingBox": [346, 63, 387, 63, 387, 76, 346, 75],
                        "confidence": 0.999,
                        "span": {"offset": 26, "length": 5},
                    },
                    {
                        "content": "C",
                        "boundingBox": [393, 63, 400, 63, 399, 76, 392, 76],
                        "confidence": 0.995,
                        "span": {"offset": 32, "length": 1},
                    },
                    {
                        "content": "DL",
                        "boundingBox": [178, 71, 192, 72, 192, 83, 178, 82],
                        "confidence": 0.994,
                        "span": {"offset": 34, "length": 2},
                    },
                    {
                        "content": "F89264518",
                        "boundingBox": [202, 72, 266, 72, 266, 85, 202, 84],
                        "confidence": 0.956,
                        "span": {"offset": 37, "length": 9},
                    },
                    {
                        "content": "Exp",
                        "boundingBox": [176, 93, 199, 91, 199, 104, 177, 106],
                        "confidence": 0.996,
                        "span": {"offset": 47, "length": 3},
                    },
                    {
                        "content": "01/01/2025",
                        "boundingBox": [202, 90, 268, 88, 267, 102, 202, 104],
                        "confidence": 0.995,
                        "span": {"offset": 51, "length": 10},
                    },
                    {
                        "content": "LN",
                        "boundingBox": [177, 116, 192, 117, 192, 130, 177, 129],
                        "confidence": 0.979,
                        "span": {"offset": 62, "length": 2},
                    },
                    {
                        "content": "Puelma",
                        "boundingBox": [201, 117, 255, 119, 254, 133, 201, 131],
                        "confidence": 0.999,
                        "span": {"offset": 65, "length": 6},
                    },
                    {
                        "content": "FN",
                        "boundingBox": [177, 132, 192, 132, 192, 146, 177, 145],
                        "confidence": 0.994,
                        "span": {"offset": 72, "length": 2},
                    },
                    {
                        "content": "Diogo",
                        "boundingBox": [203, 136, 244, 136, 244, 153, 203, 153],
                        "confidence": 0.994,
                        "span": {"offset": 75, "length": 5},
                    },
                    {
                        "content": "Andrés",
                        "boundingBox": [249, 136, 303, 137, 303, 153, 249, 153],
                        "confidence": 0.971,
                        "span": {"offset": 81, "length": 6},
                    },
                    {
                        "content": "988",
                        "boundingBox": [179, 155, 199, 155, 200, 169, 179, 168],
                        "confidence": 0.994,
                        "span": {"offset": 88, "length": 3},
                    },
                    {
                        "content": "San",
                        "boundingBox": [203, 155, 227, 155, 227, 169, 204, 169],
                        "confidence": 0.998,
                        "span": {"offset": 92, "length": 3},
                    },
                    {
                        "content": "Martín",
                        "boundingBox": [229, 155, 267, 155, 267, 170, 230, 169],
                        "confidence": 0.727,
                        "span": {"offset": 96, "length": 6},
                    },
                    {
                        "content": "Ave,",
                        "boundingBox": [270, 155, 297, 155, 297, 170, 270, 170],
                        "confidence": 0.991,
                        "span": {"offset": 103, "length": 4},
                    },
                    {
                        "content": "Apt",
                        "boundingBox": [300, 155, 321, 155, 320, 169, 300, 170],
                        "confidence": 0.999,
                        "span": {"offset": 108, "length": 3},
                    },
                    {
                        "content": "B",
                        "boundingBox": [323, 155, 331, 155, 331, 169, 323, 169],
                        "confidence": 0.994,
                        "span": {"offset": 112, "length": 1},
                    },
                    {
                        "content": "Concepción,",
                        "boundingBox": [179, 172, 251, 171, 251, 185, 179, 185],
                        "confidence": 0.599,
                        "span": {"offset": 114, "length": 11},
                    },
                    {
                        "content": "Chile,",
                        "boundingBox": [254, 171, 289, 171, 288, 185, 254, 185],
                        "confidence": 0.973,
                        "span": {"offset": 126, "length": 6},
                    },
                    {
                        "content": "98102",
                        "boundingBox": [291, 171, 327, 171, 327, 185, 291, 185],
                        "confidence": 0.999,
                        "span": {"offset": 133, "length": 5},
                    },
                    {
                        "content": "DOB",
                        "boundingBox": [178, 183, 203, 184, 203, 197, 178, 196],
                        "confidence": 0.998,
                        "span": {"offset": 139, "length": 3},
                    },
                    {
                        "content": "01/17/1990",
                        "boundingBox": [207, 184, 289, 184, 288, 199, 207, 197],
                        "confidence": 0.995,
                        "span": {"offset": 143, "length": 10},
                    },
                    {
                        "content": "RSTR",
                        "boundingBox": [178, 197, 208, 199, 207, 209, 177, 210],
                        "confidence": 0.992,
                        "span": {"offset": 154, "length": 4},
                    },
                    {
                        "content": "END",
                        "boundingBox": [347, 95, 370, 95, 370, 108, 347, 108],
                        "confidence": 0.998,
                        "span": {"offset": 159, "length": 3},
                    },
                    {
                        "content": "NONE",
                        "boundingBox": [377, 95, 412, 95, 412, 108, 377, 108],
                        "confidence": 0.994,
                        "span": {"offset": 163, "length": 4},
                    },
                    {
                        "content": "DONOR",
                        "boundingBox": [179, 223, 203, 223, 203, 231, 178, 230],
                        "confidence": 0.97,
                        "span": {"offset": 168, "length": 5},
                    },
                    {
                        "content": "SEX:",
                        "boundingBox": [227, 244, 259, 244, 259, 256, 228, 256],
                        "confidence": 0.68,
                        "span": {"offset": 174, "length": 4},
                    },
                    {
                        "content": "M",
                        "boundingBox": [262, 244, 268, 244, 268, 257, 262, 257],
                        "confidence": 0.994,
                        "span": {"offset": 179, "length": 1},
                    },
                    {
                        "content": "HGT",
                        "boundingBox": [227, 258, 252, 258, 253, 269, 227, 270],
                        "confidence": 0.996,
                        "span": {"offset": 181, "length": 3},
                    },
                    {
                        "content": "D",
                        "boundingBox": [229, 276, 235, 276, 235, 288, 229, 287],
                        "confidence": 0.885,
                        "span": {"offset": 185, "length": 1},
                    },
                    {
                        "content": "HAIR",
                        "boundingBox": [307, 244, 335, 245, 335, 256, 307, 256],
                        "confidence": 0.992,
                        "span": {"offset": 187, "length": 4},
                    },
                    {
                        "content": "BRN",
                        "boundingBox": [344, 245, 369, 245, 369, 256, 344, 256],
                        "confidence": 0.997,
                        "span": {"offset": 192, "length": 3},
                    },
                    {
                        "content": "WGT",
                        "boundingBox": [307, 258, 337, 258, 336, 270, 307, 269],
                        "confidence": 0.997,
                        "span": {"offset": 196, "length": 3},
                    },
                    {
                        "content": "EYES",
                        "boundingBox": [399, 245, 428, 245, 428, 257, 399, 257],
                        "confidence": 0.993,
                        "span": {"offset": 200, "length": 4},
                    },
                    {
                        "content": "BLK",
                        "boundingBox": [434, 245, 457, 245, 457, 257, 434, 257],
                        "confidence": 0.998,
                        "span": {"offset": 205, "length": 3},
                    },
                    {
                        "content": "ISS",
                        "boundingBox": [424, 264, 443, 264, 443, 275, 424, 275],
                        "confidence": 0.994,
                        "span": {"offset": 209, "length": 3},
                    },
                    {
                        "content": "08/08/2020",
                        "boundingBox": [424, 277, 485, 277, 486, 289, 424, 288],
                        "confidence": 0.996,
                        "span": {"offset": 213, "length": 10},
                    },
                ],
                "lines": [
                    {
                        "content": "California",
                        "boundingBox": [27, 5, 195, 5, 196, 40, 27, 40],
                        "spans": [{"offset": 0, "length": 10}],
                    },
                    {
                        "content": "DRIVER LICENSE",
                        "boundingBox": [239, 11, 380, 11, 380, 27, 239, 27],
                        "spans": [{"offset": 11, "length": 14}],
                    },
                    {
                        "content": "CLASS C",
                        "boundingBox": [345, 62, 404, 62, 404, 75, 345, 75],
                        "spans": [{"offset": 26, "length": 7}],
                    },
                    {
                        "content": "DL F89264518",
                        "boundingBox": [178, 71, 267, 72, 267, 85, 178, 83],
                        "spans": [{"offset": 34, "length": 12}],
                    },
                    {
                        "content": "Exp 01/01/2025",
                        "boundingBox": [176, 91, 268, 88, 269, 101, 176, 106],
                        "spans": [{"offset": 47, "length": 14}],
                    },
                    {
                        "content": "LN Puelma",
                        "boundingBox": [176, 115, 257, 118, 256, 133, 176, 130],
                        "spans": [{"offset": 62, "length": 9}],
                    },
                    {
                        "content": "FN",
                        "boundingBox": [177, 132, 198, 133, 198, 146, 177, 146],
                        "spans": [{"offset": 72, "length": 2}],
                    },
                    {
                        "content": "Diogo Andrés",
                        "boundingBox": [202, 136, 303, 136, 303, 153, 202, 153],
                        "spans": [{"offset": 75, "length": 12}],
                    },
                    {
                        "content": "988 San Martín Ave, Apt B",
                        "boundingBox": [178, 155, 333, 155, 333, 169, 178, 169],
                        "spans": [{"offset": 88, "length": 25}],
                    },
                    {
                        "content": "Concepción, Chile, 98102",
                        "boundingBox": [178, 171, 328, 170, 329, 184, 178, 185],
                        "spans": [{"offset": 114, "length": 24}],
                    },
                    {
                        "content": "DOB 01/17/1990",
                        "boundingBox": [177, 183, 292, 183, 292, 199, 177, 197],
                        "spans": [{"offset": 139, "length": 14}],
                    },
                    {
                        "content": "RSTR",
                        "boundingBox": [177, 196, 234, 197, 234, 210, 177, 209],
                        "spans": [{"offset": 154, "length": 4}],
                    },
                    {
                        "content": "END NONE",
                        "boundingBox": [346, 95, 415, 95, 415, 107, 346, 107],
                        "spans": [{"offset": 159, "length": 8}],
                    },
                    {
                        "content": "DONOR",
                        "boundingBox": [178, 222, 205, 222, 205, 231, 178, 230],
                        "spans": [{"offset": 168, "length": 5}],
                    },
                    {
                        "content": "SEX: M",
                        "boundingBox": [226, 244, 274, 244, 274, 257, 226, 256],
                        "spans": [{"offset": 174, "length": 6}],
                    },
                    {
                        "content": "HGT",
                        "boundingBox": [227, 258, 253, 258, 253, 269, 228, 270],
                        "spans": [{"offset": 181, "length": 3}],
                    },
                    {
                        "content": "D",
                        "boundingBox": [229, 276, 236, 276, 236, 288, 229, 287],
                        "spans": [{"offset": 185, "length": 1}],
                    },
                    {
                        "content": "HAIR BRN",
                        "boundingBox": [306, 244, 373, 244, 373, 256, 306, 256],
                        "spans": [{"offset": 187, "length": 8}],
                    },
                    {
                        "content": "WGT",
                        "boundingBox": [307, 258, 337, 259, 337, 270, 307, 270],
                        "spans": [{"offset": 196, "length": 3}],
                    },
                    {
                        "content": "EYES BLK",
                        "boundingBox": [398, 244, 462, 245, 462, 257, 398, 257],
                        "spans": [{"offset": 200, "length": 8}],
                    },
                    {
                        "content": "ISS",
                        "boundingBox": [423, 265, 445, 264, 444, 275, 423, 275],
                        "spans": [{"offset": 209, "length": 3}],
                    },
                    {
                        "content": "08/08/2020",
                        "boundingBox": [424, 276, 487, 276, 487, 288, 424, 288],
                        "spans": [{"offset": 213, "length": 10}],
                    },
                ],
                "spans": [{"offset": 0, "length": 223}],
            }
        ],
        "styles": [],
        "documents": [
            {
                "docType": "idDocument.driverLicense",
                "boundingRegions": [
                    {"pageNumber": 1, "boundingBox": [0, 0, 507, 0, 507, 310, 0, 310]}
                ],
                "fields": {
                    "Address": {
                        "type": "string",
                        "valueString": "988 San Martín Ave, Apt B Concepción, Chile, 98102",
                        "content": "988 San Martín Ave, Apt B Concepción, Chile, 98102",
                        "boundingRegions": [
                            {
                                "pageNumber": 1,
                                "boundingBox": [179, 155, 331, 155, 331, 185, 179, 185],
                            }
                        ],
                        "confidence": 0.974,
                        "spans": [{"offset": 88, "length": 50}],
                    },
                    "CountryRegion": {
                        "type": "countryRegion",
                        "valueCountryRegion": "USA",
                        "confidence": 0.989,
                    },
                    "DateOfBirth": {
                        "type": "date",
                        "valueDate": "1990-01-17",
                        "content": "01/17/1990",
                        "boundingRegions": [
                            {
                                "pageNumber": 1,
                                "boundingBox": [207, 184, 289, 184, 288, 199, 207, 197],
                            }
                        ],
                        "confidence": 0.98,
                        "spans": [{"offset": 143, "length": 10}],
                    },
                    "DateOfExpiration": {
                        "type": "date",
                        "valueDate": "2025-01-01",
                        "content": "01/01/2025",
                        "boundingRegions": [
                            {
                                "pageNumber": 1,
                                "boundingBox": [202, 90, 268, 88, 267, 102, 202, 104],
                            }
                        ],
                        "confidence": 0.984,
                        "spans": [{"offset": 51, "length": 10}],
                    },
                    "DocumentNumber": {
                        "type": "string",
                        "valueString": "F8924518",
                        "content": "F89264518",
                        "boundingRegions": [
                            {
                                "pageNumber": 1,
                                "boundingBox": [202, 72, 266, 72, 266, 85, 202, 84],
                            }
                        ],
                        "confidence": 0.989,
                        "spans": [{"offset": 37, "length": 9}],
                    },
                    "Endorsements": {
                        "type": "string",
                        "valueString": "NONE",
                        "content": "NONE",
                        "boundingRegions": [
                            {
                                "pageNumber": 1,
                                "boundingBox": [377, 95, 412, 95, 412, 108, 377, 108],
                            }
                        ],
                        "confidence": 0.989,
                        "spans": [{"offset": 163, "length": 4}],
                    },
                    "FirstName": {
                        "type": "string",
                        "valueString": "Diogo Andrés",
                        "content": "Diogo Andrés",
                        "boundingRegions": [
                            {
                                "pageNumber": 1,
                                "boundingBox": [203, 136, 303, 137, 303, 154, 203, 153],
                            }
                        ],
                        "confidence": 0.974,
                        "spans": [{"offset": 75, "length": 12}],
                    },
                    "LastName": {
                        "type": "string",
                        "valueString": "Puelma",
                        "content": "Puelma",
                        "boundingRegions": [
                            {
                                "pageNumber": 1,
                                "boundingBox": [201, 117, 255, 119, 254, 133, 201, 131],
                            }
                        ],
                        "confidence": 0.981,
                        "spans": [{"offset": 65, "length": 6}],
                    },
                    "Region": {
                        "type": "string",
                        "valueString": "California",
                        "confidence": 0.989,
                    },
                    "Sex": {
                        "type": "string",
                        "valueString": "M",
                        "content": "M",
                        "boundingRegions": [
                            {
                                "pageNumber": 1,
                                "boundingBox": [262, 244, 268, 244, 268, 257, 262, 257],
                            }
                        ],
                        "confidence": 0.987,
                        "spans": [{"offset": 179, "length": 1}],
                    },
                    "VehicleClassifications": {
                        "type": "string",
                        "valueString": "C",
                        "content": "C",
                        "boundingRegions": [
                            {
                                "pageNumber": 1,
                                "boundingBox": [393, 63, 400, 63, 399, 76, 392, 76],
                            }
                        ],
                        "confidence": 0.985,
                        "spans": [{"offset": 32, "length": 1}],
                    },
                },
                "confidence": 0.988,
                "spans": [{"offset": 0, "length": 223}],
            }
        ],
    },
}

fields = {"FirstName", "LastName", "Sex", "DateOfBirth"}
for field, value in result["analyzeResult"]["documents"][0]["fields"].items():
    if field in fields:
        print(field, value)
