# Require any additional compass plugins here.

require 'bootstrap-sass'
require 'font-awesome-sass'
require 'uglifier'
require 'pg'

# Set this to the root of your project when deployed:
http_path    = "/"
project_path = "."
css_dir      = "output/assets/style"
sass_dir     = "content/assets/style"
images_dir   = "output/assets/images"

# when using SCSS:
sass_options = {
  :syntax => :scss
}

# You can select your preferred output style here (can be overridden via the command line):
output_style = :compressed

# To enable relative paths to assets via compass helper functions. Uncomment:
relative_assets = true

# To disable debugging comments that display the original location of your selectors. Uncomment:
# line_comments = false
