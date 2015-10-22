#!env sh
# Generates 1 page document
curl -o 1page.pdf -v -X POST -F "page1=@input.svg;type=application/svg+xml" \
    -F width=0 -F height=0 -F output=1page.pdf http://localhost:8001/process
# Generates 5 page document
#curl -o 5page.pdf  -v -X POST -F "page1=@input.svg;type=application/svg+xml" \
#    -F "page2=@input.svg;type=application/svg+xml" \
#    -F "page3=@input.svg;type=application/svg+xml" \
#    -F "page4=@input.svg;type=application/svg+xml" \
#    -F "page5=@input.svg;type=application/svg+xml" \
#    -F width=0 -F height=0  -F output=5page.pdf http://localhost:8001/process
