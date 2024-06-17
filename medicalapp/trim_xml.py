import xmltodict


def trim_xml(input_file, output_file, max_entries=10000):
	with open(input_file, 'r', encoding='utf-8') as file:
		data = xmltodict.parse(file.read())
		records = data['DescriptorRecordSet']['DescriptorRecord']

		trimmed_records = records[:max_entries]

		trimmed_data = {
			'DescriptorRecordSet': {
				'DescriptorRecord': trimmed_records
			}
		}

		if '@xmlns' in data['DescriptorRecordSet']:
			trimmed_data['DescriptorRecordSet']['@xmlns'] = \
			data['DescriptorRecordSet']['@xmlns']

		# Convert back to XML
		trimmed_xml = xmltodict.unparse(trimmed_data, pretty=True)

		# Write to the output file
		with open(output_file, 'w', encoding='utf-8') as output_file:
			output_file.write(trimmed_xml)



input_file = 'desc2024.xml'
output_file = 'desc2024_trimmed.xml'
trim_xml(input_file, output_file)
