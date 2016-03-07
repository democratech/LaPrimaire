#!/usr/bin/ruby

require 'net/https'
require 'json'
require './keys.local.rb'

uri = URI.parse(SLCKHOST)
http = Net::HTTP.new(uri.host, uri.port)
http.use_ssl = true
http.verify_mode = OpenSSL::SSL::VERIFY_NONE
request = Net::HTTP::Post.new(SLCKPATH)
request.body = "payload="+JSON.dump({
	"channel"=> "#errors",
	"username"=> "monit",
	"text"=> "[#{ENV['MONIT_HOST']}] #{ENV['MONIT_SERVICE']} - #{ENV['MONIT_DESCRIPTION']}",
	"icon_emoji"=>":dog:"
})
res=http.request(request)
if not res.kind_of? Net::HTTPSuccess then
	puts "An error occurred trying to send a Slack notification\n"
end
