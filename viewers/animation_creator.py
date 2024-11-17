import matplotlib.pyplot as plt
from matplotlib import animation, rc
import matplotlib as mpl
import numpy as np
from IPython.display import HTML

class AnimationCreator:
    def __init__(self, config=None, limit_embed_MB=10.0, interval_msec=100, is_jupyter=False):
        if not config:
            raise ValueError(
                "config must be provided as a dictionary with keys: 'nrows', 'ncols', 'figsize', and optionally 'cmap'."
            )
        """
        Parameters
        ----------
        config : dict
            Configuration dictionary with the following keys:
            - 'nrows' (int): Number of rows in the grid.
            - 'ncols' (int): Number of columns in the grid.
            - 'figsize' (list or tuple): Figure size as [width, height].
            - 'cmap' (str): (Optional) Colormap name for visualization.

            Example:
            config = {'nrows': 2, 'ncols': 2, 'figsize': [8, 8], 'cmap': 'viridis'}
        """
        self.config = config
        self.cmap = config.get('cmap', 'viridis')  # Default to 'viridis' if cmap is not provided
        mpl.rcParams['animation.embed_limit'] = limit_embed_MB
        self.interval_msec = interval_msec

        self.fig, self.axes = plt.subplots(self.config['nrows'], self.config['ncols'], figsize=self.config['figsize'])
        self.axes = np.array(self.axes).flatten()  # Ensure axes are a flat array for iteration
        self.is_jupyter = is_jupyter
        if self.is_jupyter:
            plt.close(self.fig)  # Avoid duplicate rendering in Jupyter
        self.anim = None

    def create(self, images_list: list, titles=None, main_title='Animation') -> animation.FuncAnimation:
        if len(images_list) != len(self.axes):
            raise ValueError(
                f"Number of image sets ({len(images_list)}) must match the number of subplots ({len(self.axes)})."
            )
        rc('animation', html='jshtml')

        # Initialize the figure and axes
        title_text = self.fig.suptitle(main_title, fontsize=12, color='black')
        # Set individual subplot titles
        if titles:
            if len(titles) != len(self.axes):
                raise ValueError(f"Number of titles ({len(titles)}) must match the number of subplots ({len(self.axes)}).")
            for ax, title in zip(self.axes, titles):
                ax.set_title(title, fontsize=10)

        # Prepare initial frames
        artists = []
        for ax, images in zip(self.axes, images_list):
            im = ax.imshow(images[0], cmap=self.cmap)
            artists.append(im)

        frame_number_text = self.fig.text(
            0.5, 0.93, 'Frame 1', ha='center', va='center', fontsize=12, color='darkblue'
        )
        # Update function for animation
        def update(frame_idx):
            for im, images in zip(artists, images_list):
                im.set_array(images[frame_idx])
            frame_number_text.set_text(f"Frame {frame_idx + 1}")
            return artists + [frame_number_text]

        # Create animation
        self.anim = animation.FuncAnimation(
            self.fig, update, frames=len(images_list[0]), interval=self.interval_msec, blit=False
        )

        if self.is_jupyter:
            plt.close(self.fig)  # Avoid duplicate rendering in Jupyter

    def get_animation(self):
        """Getter for the created animation."""
        if self.anim is None:
            raise RuntimeError("No animation has been created. Call `create` first.")
        return self.anim

    def save(self, output_filename=None, fps=10):
        if self.anim is None:
            raise RuntimeError("No animation created. Call `create` before saving.")
        self.anim.save(filename=output_filename, writer='ffmpeg', fps=5)  # Save with 5 frames per second
        print(f"Animation saved as '{output_filename}'.")

    def show(self):
        """Display the animation."""
        if self.anim is None:
            raise RuntimeError("No animation created. Call `create` before trying to display it.")

        if self.is_jupyter:
            return HTML(self.anim.to_jshtml())
        else:
            plt.show()

if __name__ == '__main__':
    # Configuration for the animation
    config = {
        'nrows': 2,       # 2 rows
        'ncols': 2,       # 2 columns
        'figsize': [8, 8], # Size of the figure
        'cmap': 'plasma'  # Colormap (optional)
    }

    # Create an instance of AnimationCreator
    anim_creator = AnimationCreator(config=config, limit_embed_MB=20.0, interval_msec=200)

    # Generate random data (4 frames for each subplot)
    images_list = [
        [np.random.rand(10, 10) for _ in range(20)],  # Data for subplot 1
        [np.random.rand(10, 10) for _ in range(20)],  # Data for subplot 2
        [np.random.rand(10, 10) for _ in range(20)],  # Data for subplot 3
        [np.random.rand(10, 10) for _ in range(20)]   # Data for subplot 4
    ]

    # Titles for each subplot
    titles = ['Plot 1', 'Plot 2', 'Plot 3', 'Plot 4']

    # Create the animation
    anim_creator.create(images_list=images_list, titles=titles, main_title="Sample Animation")

    # Save the animation to a file
    output_filename = "animation.mp4"  # Output file name
    anim_creator.save(output_filename, fps=10)  # Save with 5 frames per second
    anim_creator.show()
