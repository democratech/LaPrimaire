require 'csv'
require 'uri'
require 'net/http'
require './keys.local.rb'

def send_entry(data) 
	uri = URI.parse(WFURL)
	http = Net::HTTP.new(uri.host, uri.port)
	http.use_ssl = true
	http.verify_mode = OpenSSL::SSL::VERIFY_NONE
	request = Net::HTTP::Post.new(WFFORMURL2)
	request.basic_auth WFKEY,WFPASS
	request.add_field('Content-Type', 'application/x-www-form-urlencoded')
	request.body = data
	return http.request(request)
end

signatures = CSV.read(ARGV[0])
supporters = []
fields=[
	"Field1",
	"Field3",
	"Field213",
	"Field214",
	"Field215",
	"Field216",
	"Field314",
	"Field315",
	"Field316",
	"Field415",
	"Field416",
	"Field417",
	"Field418",
	"Field419",
	"Field516",
	"Field517",
	"Field518",
	"Field617",
	"Field618",
	"Field10",
	"Field11",
	"Field12",
	"Field110",
	"Field111",
	"Field112",
	"Field113",
	"Field114",
	"Field115",
	"Field116",
	"Field211",
	"Field2"
]
entry_format=fields.join("=%s&")+"=%s"
signatures.each do |line|
	entry= entry_format % [
		line[1],
		line[2],
		line[3],
		line[4],
		line[5],
		line[6],
		line[7],
		line[8],
		line[9],
		line[10],
		line[11],
		line[12],
		line[13],
		line[14],
		line[15],
		line[16],
		line[17],
		line[18],
		line[19],
		line[20],
		line[21],
		line[22],
		line[23],
		line[24],
		line[25],
		line[26],
		line[27],
		line[28],
		line[29],
		line[30],
		line[31]
	]
	supporters.push(entry) unless line.empty?
end

supporters.each do |k|
	sleep(rand(3))
	res=send_entry(k)
	puts res.response
end
