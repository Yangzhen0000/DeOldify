import argparse
import glob
from tqdm import tqdm
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
# arguments for image colorization
parser.add_argument('--artistic', default=True, action='store_true',
                    help='True for artistic mode and False for stable')
parser.add_argument('--source_path', default='./test_images',
                    help='path of input images')
# arguments for video colorization
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
    #source_url = 'https://upload.wikimedia.org/wikipedia/commons/e/e4/Raceland_Louisiana_Beer_Drinkers_Russell_Lee.jpg'
    if args.source_path is None:
        raise ValueError('You should provide source_path')
    if os.path.isdir(args.source_path):
        image_path_list = glob.glob(args.source_path+"/*")
    else:
        image_path_list = [args.source_path]


    if args.source_url is not None:
        colorizer.plot_transformed_image_from_url(url=args.source_url, 
            path=args.source_path, render_factor=args.render_factor, compare=True)
    else:
        tqdm_test = tqdm(image_path_list, ncols=80)
        for idx, image_path in enumerate(tqdm_test):
            colorizer.plot_transformed_image(path=image_path,
                render_factor=args.render_factor, compare=True)
elif args.input_type == "video":
    colorizer = get_video_colorizer()
    if args.render_factor is None:
        args.render_factor = 21
    if args.filename is None:
        raise ValueError('You should provide video filename')
        # source_url = 'https://twitter.com/silentmoviegifs/status/1116751583386034176'
        # file_name = 'DogShy1926.mp4'

    if args.source_url is not None:
        colorizer.colorize_from_url(args.source_url, args.filename, render_factor=args.render_factor)
    else:
        colorizer.colorize_from_file_name(args.filename)
else:
    raise NotImplementedError('You can only choose from [video] or [image]'.format(args.input_type))
