import argparse
import logging
import coloredlogs

def run(*args, **kwargs):
    print(*args, **kwargs)
    parser = argparse.ArgumentParser(description='imgUtils is an advanced image-modification utility written in Python.')
    parser.add_argument("input", help="The file or folder to use")
    parser.add_argument("output", nargs = "?", help="The filename to output to. This is overridden by -r in single-file mode, and need not be specified in that case.")
    parser.add_argument("-r", "--rename", nargs="+", metavar=("REPLACE", "(optional) REGEX"), help="Replace instances of text that match REGEX in the name of the image(s) with REPLACE. (If REGEX is not specified, it will use the filename verbatim.) REPLACE can contain these percent codes: %%(counter)s is replaced with a number th at starts at 0 and increases for each image. %%(datetime)s will be replaced with the date and time. %%(uuid)s will be replaced with a random UUID.")
    parser.add_argument("-wm", "--watermark", nargs = "+", metavar = ("PATH", "TRANSPARENCY"), help="Adds a watermark to the image(s). If specified, TRANSPARENCY should be a number from 0 to 1, and defaults to 0.5.")
    parser.add_argument("-wc", choices = ["ul", "ur", "bl", "br"], default = "br", help="The corner to add a watermark to. Defaults to br.")
    parser.add_argument("-zip", action="store_true", help="Compresses the input folder to a zipfile.")
    parser.add_argument("-rt", "--rotate", metavar="ANGLE", type=int, help="Rotates the image(s) by a given angle.(Note: If rotating at 90 degree angles, it is usually simpler to use -tr)")
    parser.add_argument("-rtx", action="store_true", help="If specified with -rt, the rotated image will be expanded to contain the entire image, instead of being cut off at the corners.")
    parser.add_argument("-tr", "--transpose", action="append", choices=["flip-horizontal", "flip-vertical", "rotate-90", "rotate-180", "rotate-270"], help="Applies the given transformation to the image(s). (Note: This flag can be specified multiple times, and each action will be applied in the order they were passed)")
    parser.add_argument("-fx", "--effects", choices=["blur", "countour", "detail", "edge-enhance", "edge-enhance-more", "emboss", "find-edges", "sharpen", "smooth", "smooth-more"], help="Apply the given effect to the image(s).")
    parser.add_argument("-rs", "--resize", nargs=2, metavar=("WIDTH", "HEIGHT"), help="Resizes the image to a given width/height. (Note: To resize an image for something like  thumbnail, use -t)")
    parser.add_argument("-t", "--thumbnail", type=int, metavar="SIZE", help="Resize the image to the given size, while preserving aspect ratio.")
    parser.add_argument("-v", action="store_true", help="Activate verbose mode.")

    args = parser.parse_args()

    coloredlogs.install(level = "DEBUG" if args.v else "INFO")

    logging.debug("imgUtils starting...")
    logging.debug(args)
    import PIL
    from PIL import Image
    from zipfile import ZipFile
    import os
    from pathlib import Path
    import sys
    from datetime import datetime
    from uuid import uuid4
    import re

    logging.info("Loading input data")
    try:
      path = Path(args.input)
    except:
      logging.error("Invalid path: " + str(path))
      sys.exit(-3)
    if not path.exists():
      logging.error("File does not exist: " + str(path))
      sys.exit(-3)
    logging.debug("Checking input filetype")
    pathtype = None
    if path.is_dir():
      pathtype = "dir"
    else:
      pathtype = "file"
    logging.debug("Type: " + pathtype)
    files = []
    if pathtype == "file":
      files.append(path)
    elif pathtype == "dir":
      for item in os.listdir(path):
        files.append(item)
      os.mkdir(args.output)
      os.chdir(path)
    logging.info("Total " + str(len(files)) + " files to process")
    logging.debug(files)
    if args.zip:
      if not args.output:
        logging.error("Output name not specified!")
      logging.debug("Preparing zipfile")
      zipfile = ZipFile(args.output + ".zip", mode="w")
      if len(files) == 1:
        logging.warning("The zipfile that will be created will contain only one image.")

    counter = 0
    for item in files:
      logging.info("Loading file")
      try:
        img = Image.open(path)
      except PIL.UnidentifiedImageError as e:
        logging.error(e)
        sys.exit(-2)
      logging.info("Processing file #" + str(counter + 1))
      if args.transpose:
        logging.info("Transposing image...")
        key = {"flip-horizontal": Image.FLIP_LEFT_RIGHT, "flip-vertical": Image.FLIP_TOP_BOTTOM, "rotate-90": Image.ROTATE_90, "rotate-180": Image.ROTATE_180, "rotate-270": Image.ROTATE_270}
        for item in args.transpose:
          logging.debug("Applying " + item)
          img = img.transpose(key[item])
      if args.rotate:
        logging.info("Rotating image...")
        img = img.rotate(args.rotate, expand = args.rtx)
      if args.watermark != None:
        logging.info("Adding watermark...")
        try:
          watermark = Image.open(args.watermark[0])
        except:
          logging.error("Invalid watermark file!")
          sys.exit(-4)
        try:
          trans = float(args.watermark[1])
          if not trans <= 1 and trans >= 0:
            logging.error("Invalid valuue for transparency!")
            sys.exit(-4)
          watermark.putalpha(int(255 * trans))
        except IndexError:
          watermark.putalpha(127)
        except ValueError:
          logging.error("Invalid value for transparency!")
          sys.exit(-4)
        width, height = img.size
        markWidth, markHeight = watermark.size
        pos = None
        argpos = args.wc
        if argpos == "br":
          pos = (width - markWidth, height - markHeight)
        elif argpos == "bl":
          pos = (0, height - markHeight)
        elif argpos == "tl":
          pos = (0, 0)
        elif argpos == "tr":
          pos = (width - markWidth, 0)
        logging.debug("Calculated pos: " + str(pos))
        img.paste(watermark, pos, watermark)
      if args.rename:
        logging.debug("Creating new name...")
        try:
          name = args.rename[0] % {"counter": str(counter), "datetime": datetime.now().strftime("%I-%M-%S-%P-%-m-%d-%Y"), "uuid": str(uuid4())}
        except ValueError:
          logging.error("Error formatting name. Did you put 's' after the format codes? (i.e. %%(uuid)s)")
          sys.exit(-4)
        if len(args.rename) == 2:
          name = re.sub(args.rename[1], args.rename[0])
      else:
        name = args.output
      logging.debug(name)
      if args.resize:
        logging.info("Resizing...")
        logging.debug(args.resize)
        img = img.resize(args.resize[0], args.resize[1])
      if args.thumbnail:
        img.thumbnail((args.thumbnail, args.thumbnail))
      logging.info("Saving image...")
      try:
        if pathtype == "dir":
          img.save(args.output + "/" + name)
        else:
          img.save(name)
      except ValueError:
        logging.error("Failed to save image! Did you provide a file extension in the name?")
        sys.exit(-2)
      if args.zip:
        zipfile.write(name)
      counter += 1
    zipfile.close()
    logging.info("Completed! Succesfully applied operations on " + str(counter) + " file(s).")