import xml.etree.ElementTree as ET

def compute_function_coverage(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    total_functions = 0
    covered_functions = 0

    for cls in root.findall(".//class"):
        for function in cls.findall("function"):
            total_functions += 1
            if int(function.get("line-rate")) > 0:
                covered_functions += 1

    coverage_percentage = (covered_functions / total_functions) * 100 if total_functions else 0
    return covered_functions, total_functions, coverage_percentage

xml_path = 'coverage.xml'  # 默认的输出文件名
covered, total, percentage = compute_function_coverage(xml_path)
print(f"Total functions: {total}")
print(f"Covered functions: {covered}")
print(f"Function coverage: {percentage:.2f}%")