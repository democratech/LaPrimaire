require 'csv'
require 'mailgun'

signatures = CSV.read('signatures.csv')
sigs = {}
signatures.each do |line|
	msg=line[5]
	if not line[3].nil? then
		line[3]=line[3].capitalize
	end
	if not line[0].nil? then
		line[0]=line[0].capitalize
	end
	if not line[1].nil? then
		line[1]=line[1].upcase
	end
	if msg.nil? then
		msg="J'approuve votre initiative mais je n'ai pas mis de message :)\n\n%s %s - %s (%s)" % [line[0],line[1],line[3],line[4]]
	else
		msg+="\n\n%s %s - %s (%s)" % [line[0],line[1],line[3],line[4]]
	end
	sigs[line[2]]={:firstname=>line[0],:lastname=>line[1],:email=>line[2],:city=>line[3],:zip=>line[4],:msg=>msg}
end

sigs.each do |k,v|
	sleep(rand(10))
	mg_client = Mailgun::Client.new "key-XXXXXXXX"
	message_params = {:from    => k,  
		  :to      => 'hello@democratech.co',
		  :subject => 'Nouvelle signature !',
		  :text    => v[:msg]}
	mg_client.send_message "mail.domain.com", message_params
end
