# All files in the 'lib' directory will be loaded
# before nanoc starts compiling.

require 'nanoc/cachebuster'
include Nanoc::Helpers::CacheBusting
include Nanoc::Helpers::LinkTo
include Nanoc::Helpers::Rendering
