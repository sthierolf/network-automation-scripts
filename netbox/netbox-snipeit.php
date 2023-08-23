<?php
#
# Initialize a snipeit array with token and URL to location API function
#
$snipeit = Array(
	'token' => 'Bearer API_TOKEN_GOES_HERE
	'accept' => 'application/json',
	'content-type' => 'application/json',
	'url' => 'https://SNIPEIT_FQDN/api/v1/locations?limit=1&offset=0&search=',
);
#
# Verify if a location parameter is passed as HTTP GET
#
if(isset($_GET['location'])) {
	#
	# Set CURL options and get data
	#
	$ch = curl_init($snipeit['url'] . $_GET['location']);
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($ch, CURLOPT_HEADER, 0);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, 1);
	curl_setopt($ch, CURLOPT_URL, $snipeit['url'] . $_GET['location']);
	curl_setopt($ch, CURLOPT_HTTPHEADER, Array('authorization: ' . $snipeit['token']));
	$data = curl_exec($ch);
	#
	# If CURL returns HTTP status code 200 (OK), then we can
	# parse the json data and redirect to Snipe-IT location
	#
	if(curl_getinfo($ch, CURLINFO_HTTP_CODE) == 200){
		#
		# use json data as object
		#
		$object = json_decode($data);
			#
			# DEBUG to verify output
			#
			#print_r($object);
			#print $object->rows[0]->id;
		#
		# Do an HTTP redirect to Snipe-IT location by the ID
		#
		$redirect = 'Location: https://SNIPEIT_FQDN/locations/' . $object->rows[0]->id;
		header($redirect);
		exit;
	}
	curl_close($ch);
}
?>