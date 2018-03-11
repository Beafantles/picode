# picode

Picode is a Python library (and will also be a command-line tool) which can convert codes to pictures.

This project is inspired from [carbon](https://carbon.now.sh).

I wanted to create nice overviews for my project [Discode](https://github.com/Beafantles/Discode) so I made it.

## Installing

Just open a terminal and type:

```bash
pip install -U picode
```

## How does it work?

This project uses [pygments](http://pygments.org/) for syntax highlighting and [pillow](https://pillow.readthedocs.io/en/latest/) for processing images.

### Basic example

Here's a short example:

```py
import picode

image_1 = picode.to_pic(file_path="main.cpp")
image_2 = picode.to_pic(code="#!python\nprint('Hello world!')")

image_1.save("image_1.png")
image_2.save("image_2.png")
```

Here's `main.cpp`:

```cpp
#include <iostream>

int main()
{
    std::cout << "Hello world!\n";
    return 0;
}
```

Here's `image_1.png`:

![image_1.png](https://i.imgur.com/cdmF5Jq.png)

Here's `image_2.png`:

![image_2.png](https://i.imgur.com/iuCu6LF.png)

### Documentation

Consult the [docs](https://github.com/Beafantles/picode/wiki) for more information about how to use it.

## Ideas / Improvements

⚠️ **I don't work on this project on a regular basis but rather when I want to. Don't expect any precise date for these features / ideas to be released.** ⚠️

- Command-line tool (registered in PATH)
- Upload the picture to [imgur](imgur.com)
- Copy the picture / picture's link to the clipboard
- Keyboard shortcuts
- Custom default style

## Contributing

Feel free to submit improvements / features / ideas by creating an issue to this project.

If you see any bugs, please create an issue with the details.

If you wanna merge your improvments, please ensure your code respects Google's formatting style by running `beautify.bat` if you're on Windows or `beautify.sh` if you're on Linux. You must have [yapf](https://github.com/google/yapf) installed to run these scripts.

## Known issues

The parameter `show_lines_numbers` has no effect at the moment. It's apparently a problem from `pygments` library. I opened an [issue](https://bitbucket.org/birkenfeld/pygments-main/issues/1426/line-number-separator-always-displayed) and I hope this this will be fixed soon.

`pygments` seems to have some difficulties to detect which language is used according to a provided code / file. To avoid incorrect syntax highlighting, you can explicitly specify the language using the `language` parameter.

Some tokens aren't recognized as they should do. It causes some issues with the syntax highlighting (some elements aren't colorized as they should be). It seems to be a problem with `pygments`. I opened an [issue](https://bitbucket.org/birkenfeld/pygments-main/issues/1427/error-in-documentation-for-the-token) and I hope this will be fixed soon.

## Changelog

**11/03/2018**

First version of the project, providing a basic Python library.