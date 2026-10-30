#!/bin/bash

freeze --execute "onefetch --disabled-fields head authors last-change url lines-of-code churn --no-title" --border.width 10 --output doc/app_presentation.svg

git add doc/*.svg
