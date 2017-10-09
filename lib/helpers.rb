# All files in the 'lib' directory will be loaded
# before nanoc starts compiling.

require 'nanoc/cachebuster'
require_relative '../config/keys.local.rb'
include Nanoc::Helpers::CacheBusting
include Nanoc::Helpers::LinkTo
include Nanoc::Helpers::Rendering
include Nanoc3::Helpers::XMLSitemap

def create_robots_txt
	if @site.config[:robots]
		content = if @site.config[:robots][:default]
				  <<-EOS
User-agent: *
Disallow: /admin/
Disallow: /citoyen/
Noindex: /qualifie/roxane-revon
Noindex: /candidat/205888341238
EOS
			  else
				  [
					  'User-Agent: *',
					  @site.config[:robots][:disallow].map { |l| "Disallow: #{l}" },
					  (@site.config[:robots][:allow] || []).map { |l| "Allow: #{l}" },
					  "Sitemap: #{@site.config[:robots][:sitemap]}"
				  ].flatten.compact.join("\n")
				  end
		@items << Nanoc3::Item.new(
			content,
			{ :extension => 'txt', :is_hidden => true },
			'/robots/'
		)
	end
end


def create_sitemap
	@items.each do |item|
		if %w{png gif jpg jpeg coffee scss sass less css xml js txt}.include?(item[:extension]) ||
			item.identifier =~ /404|500|htaccess/
			item[:is_hidden] = true unless item.attributes.has_key?(:is_hidden)
		end
	end
	@items << Nanoc3::Item.new(
		"<%= xml_sitemap %>",
		{ :extension => 'xml', :is_hidden => true },
		'/sitemap/'
	)
end

def create_candidats
	page={
		'title'=>"La Primaire Citoyenne pour l'élection présidentielle de 2017 - LaPrimaire.org",
		'social_title'=>"LaPrimaire.org - Pour un VRAI choix en 2017 !",
		'image'=>"https://s3.eu-central-1.amazonaws.com/laprimaire/laprimaire-banner-rectangle.jpg",
		'footer'=>true,
		'navbar'=>true,
		'author'=>"des citoyens ordinaires",
		'description'=>"LaPrimaire.org est une Primaire citoyenne ouverte organisée hors des partis politiques pour les élections de 2017. La Primaire vise à rassembler les citoyens déçus et lassés des politiques et qui souhaitent redonner du sens aux élections en soutenant et participant à une grande primaire citoyenne, apartisane, ouverte, en 2017 afin d'élire des candidats vraiment représentatifs."
	}
	@db=PG.connect(
		"dbname"=>DBNAME,
		"user"=>DBUSER,
		"password"=>DBPWD,
		"host"=>DBHOST, 
		"port"=>DBPORT
	)
	q="SELECT * FROM candidates WHERE qualified"
	res=@db.exec(q)
	@db.close
	if res.num_tuples>0 then
		res.each do |r|
			name=r['name'].downcase.gsub(' ','-')
			r['firstname']=r['name'].split(' ',2)[0].downcase.capitalize
			r['lastname']=r['name'].split(' ',2)[1].downcase.capitalize
			r.merge!(page)
			@items << Nanoc::Item.new('', r, "/qualifie/#{name}/")
		end
	end
end
