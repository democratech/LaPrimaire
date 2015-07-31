nanoc-skeleton
==============

[![Dependency Status](https://gemnasium.com/alessandro1997/nanoc-skeleton.svg)](https://gemnasium.com/alessandro1997/nanoc-skeleton)

[nanoc-skeleton](https://github.com/alessandro1997/nanoc-skeleton) is a starter
template for the [nanoc](https://nanoc.ws) static website generator.

## Features

This starter template provides the following features out of the box:

  - [Compass](http://compass-style.org/)
  - [bootstrap-sass](https://github.com/twbs/bootstrap-sass)
  - [Bootstrap's JavaScript](http://getbootstrap.com/javascript) (through a CDN)
  - [guard-nanoc](https://github.com/guard/guard-nanoc)

## Usage

Using this template is pretty simple:

```console
$ git clone git://github.com/alessandro1997/nanoc-skeleton.git
$ cd nanoc-skeleton
$ bundle install
$ bundle exec guard
```

This will compile your new shining nanoc site and start watching for changes.

To start a web server run:

```console
$ bundle exec nanoc view
```

You can now access your site at [http://localhost:3000](http://localhost:3000)!

## Assets

To customize your site, open ```content/assets/styles/main.scss```. By default
it should look something like this:

```scss
@import "bootstrap/bootstrap";

body {
  padding-top: 60px;
}
```

You're free to edit ```main.scss``` directly, but we recommend splitting your
layout into separate files.

### Assets compilation

All assets beginning with an underscore will not be routed by nanoc. This allows
you to output your CSS in a single file while providing the benefit of multiple
stylesheets.

For example, you can put all your mixins into a ```_mixins.scss``` file. Then,
wherever you want to use them, you can import the file:

```scss
@import "mixins";

// ...
```

Nice, right?

## Contributing

1. [Fork it](http://github.com/alessandro1997/nanoc-skeleton/fork)
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request

## Authors

nanoc-skeleton is developed and mantained by [Alessandro Desantis](http://alessandro1997.github.io).

## License

nanoc-skeleton is released under the [MIT license](https://github.com/alessandro1997/nanoc-skeleton/blob/master/LICENSE.txt).
