require 'nanoc'

module Nanoc
	module Filters
		class ConcatFilter < Nanoc::Filter
			identifier :concat
			def run(content, args = {})
				return unless item[:require]
				rel_folder = File.dirname(@item.identifier.chop)
				includes = ""
				for name in item[:require] or []
					included_item = @items["#{rel_folder}/#{name}/"]
					includes << included_item.compiled_content + "\n;"
				end
				includes + content
			end
		end
	end
end
