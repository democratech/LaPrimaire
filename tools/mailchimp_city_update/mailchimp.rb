require 'csv'
require 'uri'
require 'net/http'
require 'json'

MCKEY = 'XXXXXXXXXXXXX-us10'
MCURL = 'https://XXX.api.mailchimp.com'
MCLIST = 'XXXXXXXX'
code_postaux=CSV.read('code_postaux_v201410.csv',:col_sep=>';')
zipcodes={}
code_postaux.each do |line|
	if zipcodes[line[2]].nil? then
		zipcodes[line[2]]=[]
	end
	zipcodes[line[2]].push(line[1].strip)
end

def update_member(id,member) 
	uri = URI.parse(MCURL)
	http = Net::HTTP.new(uri.host, uri.port)
	http.use_ssl = true
	http.verify_mode = OpenSSL::SSL::VERIFY_NONE
	request = Net::HTTP::Patch.new("/3.0/lists/"+MCLIST+"/members/"+id)
	request.basic_auth 'hello',MCKEY
	request.add_field('Content-Type', 'application/json')
	request.body = member
	return http.request(request)
end

def get_members()
	uri = URI.parse(MCURL)
	http = Net::HTTP.new(uri.host, uri.port)
	http.use_ssl = true
	http.verify_mode = OpenSSL::SSL::VERIFY_NONE
	request = Net::HTTP::Get.new("/3.0/lists/"+MCLIST+"/members")
	request.basic_auth 'hello',MCKEY
	return http.request(request)
end

res=get_members()
if not res.nil? then
	members = JSON.parse(res.body)
	members['members'].each do |m|
		info=m['merge_fields']
		if info['CITY'].empty? and not info['ZIPCODE'].empty? then
			info['ZIPCODE']=info['ZIPCODE'].delete(' ')
			if not info['ZIPCODE'].match('^[0-9]{5}(?:-[0-9]{4})?$').nil? and not zipcodes[info['ZIPCODE']].nil? then
				m['merge_fields']['CITY']=zipcodes[info['ZIPCODE']][0]
				m['merge_fields']['ZIPCODE']=info['ZIPCODE']
				res=update_member(m['id'],JSON.dump(m))
			end
		end
	end
end
