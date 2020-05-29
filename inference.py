import argparse
from deoldify import device
from deoldify.device_id import DeviceId
device.set(device=DeviceId.GPU0)

from deoldify.visualize import *
plt.style.use('dark_background')

parser = argparse.ArgumentParser()
parser.add_argument('--input_type', default='image',
                    help='image for image colorization, video for video colorization')
parser.add_argument('--render_factor', type=int, default=None,
                    help='determine the resolution at which the color portion of the video is rendered')
parser.add_argument('--source_url', default=None,
                    help='url for online image or video')
parser.add_argument('--result_path', default='./result',
                    help='path to save the results')
# arguments for image colorization
parser.add_argument('--artistic', default=True, action='store_true',
                    help='True for artistic mode and False for stable')
parser.add_argument('--source_path', default=None,
                    help='path of input images')
# argumnets for video colorization
parser.add_argument('--filename', default=None,
                    help='file name of input video, with extension')
args = parser.parse_args()

if args.input_type == "image":
    torch.backends.cudnn.benchmark=True

    colorizer = get_image_colorizer(artistic=args.artistic)

    #NOTE:  Max is 45 with 11GB video cards. 35 is a good default
    if args.render_factor is None:
        args.render_factor=35
    #NOTE:  Make source_url None to just read from file at ./video/source/[file_name] directly without modification
    source_url = 'https://upload.wikimedia.org/wikipedia/commons/e/e4/Raceland_Louisiana_Beer_Drinkers_Russell_Lee.jpg'
    source_path = 'test_images/image.png'
    result_path = None

    if source_url is not None:
        result_path = colorizer.plot_transformed_image_from_url(url=source_url, path=source_path, render_factor=render_factor, compare=True)
    else:
        result_path = colorizer.plot_transformed_image(path=source_path, render_factor=render_factor, compare=True)
    print("Image successfully saved as {:s}".format(result_path))

elif args.input_type == "video":
    colorizer = get_video_colorizer()
    if args.render_factor is None:
        args.render_factor = 21
    if args.source_url or args.filename is None:
        source_url = 'https://twitter.com/silentmoviegifs/status/1116751583386034176'
        file_name = 'DogShy1926.mp4'
    result_path = None

    if args.source_url is not None:
        result_path = colorizer.colorize_from_url(args.source_url, args.filename, render_factor=args.render_factor)
    else:
        result_path = colorizer.colorize_from_file_name(args.filename)
    show_video_in_notebook(result_path)
else:
    raise NotImplementedError('You can only choose from [video] or [image]'.format(args.input_type))