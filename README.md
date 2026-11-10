# Cultivating Community site

Jekyll site for Cultivating Community. Pushes to `main` deploy to GitHub Pages:
https://cousingus.github.io/ccv-site/

## Run locally

Requires Ruby 3.4 (see `.ruby-version`) and Bundler.

```sh
bundle config set --local path vendor/bundle
bundle install
bundle exec jekyll serve --livereload
```

Then open http://127.0.0.1:4000/ccv-site/ (note the `/ccv-site/` path).

## Editing

- Pages: `about.md`, `programs.md`, `events.md`, `shop.md`, `volunteer.md`, `donate.md`
- Navigation: `_data/navigation.yml`
- Styles: `assets/css/main.css`
- Internal links and assets must use the `relative_url` filter, so they keep working when `baseurl` changes.

## Moving to the custom domain

1. Add a `CNAME` file containing `foodsovereigntyforall.com`.
2. In `_config.yml`, set `url` to `https://foodsovereigntyforall.com` and `baseurl` to `""`.
3. Update the domain's DNS to point at GitHub Pages.
