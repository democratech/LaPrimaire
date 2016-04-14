# All files in the 'lib' directory will be loaded
# before nanoc starts compiling.

require 'nanoc/cachebuster'
include Nanoc::Helpers::CacheBusting
include Nanoc::Helpers::LinkTo
include Nanoc::Helpers::Rendering
include Nanoc3::Helpers::XMLSitemap

def create_robots_txt
	if @site.config[:robots]
		content = if @site.config[:robots][:default]
				  <<-EOS
User-agent: *
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

