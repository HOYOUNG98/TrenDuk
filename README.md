# TrenDuk

What moves are popular? Visit https://www.trenduk-go.com!

## What is TrenDuk?

This website my personal project driven by motivation to reveal the change AlphaGo brought to the Go industry. It specifically visualizes frequency of each joseki
each year. I am aiming to show more visualization with a detailed categorization.

## Stack Usage

This application is separated in 3 parts: service, web, and api. Service portion is solely built with only python, with usage of web scraping. I have not deployed it since it is very costly on operations. The web is built with Typescript React and api is built with Typescript NodeJS.

## Version

Currently, I deployed the first version, and I am working on improvements!

### Expectations for Version 0.2.0

- Hover Feature
  - When hovering a specific move on board, corresponding line on the graph will be highlighted
- Move Selection Tree
  - After selection of a move, it now will be allowing going back a move
- Loading Feature
  - Data takes a long time to load. As a result, it will be displaying a loading spinner during fetching period.
