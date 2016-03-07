require 'csv'
require 'uri'
require 'net/http'
require './keys.local.rb'

def send_entry(data) 
	uri = URI.parse(WFURL)
	http = Net::HTTP.new(uri.host, uri.port)
	http.use_ssl = true
	http.verify_mode = OpenSSL::SSL::VERIFY_NONE
	request = Net::HTTP::Post.new(WFFORMURL)
	request.basic_auth WFKEY,WFPASS
	request.add_field('Content-Type', 'application/x-www-form-urlencoded')
	request.body = data
	return http.request(request)
end

signatures = CSV.read(ARGV[0])
sigs = []
signatures.each do |line|
	if not line[3].nil? then
		line[3]=URI.escape(line[3].capitalize)
	end
	if not line[0].nil? then
		line[0]=URI.escape(line[0].capitalize)
	end
	if not line[1].nil? then
		line[1]=URI.escape(line[1].upcase)
	end
	if not line[2].nil? then
		line[2]=URI.escape(line[2])
	end
	if not line[4].nil? then
		line[4]=URI.escape(line[4])
	end
	if not line[5].nil? then
		msg=URI.escape(line[5])
	end
	entry= WFPARAMS % [line[0],line[1],line[2],line[3],line[4],msg]
	sigs.push(entry)
end

sigs.each do |k|
	sleep(rand(3))
	res=send_entry(k)
	puts res.response
end
