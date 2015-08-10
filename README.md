# democratech website

This is the code of democratech's website.
It is a static website created with the [Nanoc](http://nanoc.ws/), a ruby static site generator that has been chosen for its accessibility and ease of use and [nanoc-skeleton](https://github.com/alessandro1997/nanoc-skeleton) as a starter template to provide Bootstrap goodness.

## Usage

Firing up a copy of democratech's website on your local computer is easy:

```console
$ git clone git://github.com/democratech/website.git
$ cd website
$ bundle install
$ bundle exec guard
```

This will compile your new shining nanoc site and start watching for changes.

To start a web server run:

```console
$ bundle exec nanoc view
```

You can now access your local copy of democratech's website at [http://localhost:3000](http://localhost:3000)!

## Contributing

1. [Fork it](http://github.com/democratech/website/fork)
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create a new Pull Request

## Authors

So far, democratech's website is being developed and mantained by
* [Thibauld Favre](https://twitter.com/thibauld)
* [Jean-Tristan Chanègue](https://www.linkedin.com/in/jeantristanchanegue)
* Feel free to join us! 


## License

* democratech website is released under the [GNU Affero GPL](https://github.com/democratech/website/blob/master/LICENSE)
* nanoc-skeleton is released under the [MIT license](https://github.com/alessandro1997/nanoc-skeleton/blob/master/LICENSE.txt).
* nanoc is released under a [Free Software license] (https://github.com/nanoc/nanoc/blob/master/LICENSE).
* bootstrap is released under the [MIT license](https://github.com/twbs/bootstrap/blob/master/LICENSE).

