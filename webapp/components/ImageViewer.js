import React, { Component } from 'react';
import Icon from '@material-ui/core/Icon';
import Zoom from '@material-ui/core/Zoom';
import { withStyles } from '@material-ui/core/styles';
import CircularProgress from '@material-ui/core/CircularProgress';

const styles = theme => ({
  root: {
    height: '100%',
    display: 'flex',
    cursor: 'pointer',
    alignItems: 'center',
    backgroundColor: 'black',
    justifyContent: 'space-between',
  },
  img: {
    userSelect: 'none',
    height: '100%',
    pointerEvents: 'none',
  },
  arrowRight: {
    opacity: 1.0,
    marginRight: '10px',
    pointerEvents: 'none',
  },
  arrowLeft: {
    opacity: 1.0,
    marginLeft: '10px',
    pointerEvents: 'none',
  },
  watermarkLeft: {
    position: 'absolute',
    left: '15px',
    bottom: '5px',
  },
  watermarkRight: {
    position: 'absolute',
    right: '15px',
    bottom: '5px',
  },
  spinner: {
    color: 'dimgray',
    animationDuration: '550ms',
    position: 'absolute',
    top: '20px',
    right: '13px',
  },
  download: {
    top: '20px',
    left: '40px',
    opacity: 1.0,
    position: 'absolute',
  },
  play: {
    top: '20px',
    left: '16px',
    opacity: 1.0,
    position: 'absolute',
  },

});

function extractImageSeriesPaths (instancePath) {
  const projectId = Project.getId();
  const [nwbfile, interfase, ...name] = instancePath.split('.');

  const num_samples_var = Instances.getInstance(instancePath).getType().getVariables().find(v => v.getName() == 'num_samples');
  const num_samples = parseInt(num_samples_var.getInitialValue().value.text);

  return new Array(num_samples).fill(0).map((el, index) => `api/image?name=${name.join()}&interface=${interfase}&projectId=${projectId}&index=${index}&clientId=${GEPPETTO.MessageSocket.getClientID()}`);
}

function extractImageSeriesTimestamps (instancePath) {
  const timestamps = Instances.getInstance(`${instancePath}.timestamps`);
  const values = timestamps.getInitialValue()[0].value.value;

  if (!values) {
    // If no timestamps
    const num_samples_var = Instances.getInstance(instancePath).getType().getVariables().find(v => v.getName() == 'num_samples');
    const num_samples = parseInt(num_samples_var.getInitialValue().value.text);
    return new Array(num_samples).fill(0).map((el, index) => index);
  }

  return values.map(timestamp => new Date(parseFloat(timestamp) * 1000).toString().replace(/\(.*\)/g, ''));
}

class ImageViewer extends Component {
  cachedImage = [];

  headerButtons = ['download', 'play', 'pause'];

  showNextImage = this.showNextImage.bind(this);

  imagePaths = []

  constructor (props) {
    super(props);

    this.state = {
      activeStep: 0,
      imageLoading: true,
    };
  }

  componentDidMount () {
    
  }

  componentDidUpdate () {
    if (this.state.imageLoading && this.cachedImage[this.state.activeStep]) {
      this.setState({ imageLoading: false });
    }
  }

  handleNext = step => {
    const { activeStep } = this.state;
    const { timestamps } = this.props;

    let nextImageIndex = activeStep + step;
    if (nextImageIndex == timestamps.length) {
      nextImageIndex = 0;
    } else if (nextImageIndex < 0) {
      nextImageIndex = timestamps.length - 1;
    }

    this.setState({
      activeStep: nextImageIndex,
      imageLoading: !this.cachedImage[nextImageIndex],
    });
  }

  clickImage = (e, num_samples) => {
    const { activeStep } = this.state;
    const { offsetX } = e.nativeEvent;
    const { offsetWidth } = e.target;
    const { className } = e.target;

    if (!this.headerButtons.some(iconName => className.includes(iconName))) {
      if (offsetX > offsetWidth / 2) {
        this.handleNext(+1);
      } else {
        this.handleNext(-1);
      }
    }
  }

  showNextImage () {
    const { timestamps } = this.props;
    const { activeStep, imageLoading } = this.state;

    const nextImageIndex = activeStep < timestamps.length - 1 ? activeStep + 1 : 0;
    if (!this.cachedImage[activeStep]) {
      this.setState({ imageLoading: true });
      return;
    }

    this.setState({ activeStep: nextImageIndex, imageLoading: !this.cachedImage[nextImageIndex] });
  }

  onLoadImage (imageIndex) {
    // hide spinning wheel

    if (this.state.imageLoading && this.cachedImage[imageIndex]) {
      this.setState({ imageLoading: false });
    }
    this.cachedImage[imageIndex] = true;
  }

  autoPlay () {
    if (this.interval) {
      clearInterval(this.interval);
      this.interval = null;
    } else {
      this.showNextImage();
      this.interval = setInterval(this.showNextImage, 500);
    }
    this.setState(({ autoplayToggled }) => ({ autoplayToggled: !autoplayToggled }));
  }

  render () {
    const { instancePath, classes } = this.props;
    const { activeStep, hoverImg, imageLoading, autoplayToggled, } = this.state;

    const imagePaths = extractImageSeriesPaths(instancePath);
    this.cachedImage = imagePaths.map(() => false);
    const timestamps = extractImageSeriesTimestamps(instancePath);

    return (
      <div
        className={classes.root}
        onClick={e => this.clickImage(e, timestamps.length)}
        onMouseEnter={() => this.setState({ hoverImg: true })}
        onMouseLeave={() => this.setState({ hoverImg: false })}
      >

        <Zoom in={hoverImg} timeout={200}>
          <div className={classes.arrowLeft}>
            <Icon className="fa fa-chevron-left imgBtn" />
          </div>
        </Zoom>

        { this.renderImages() }

        {imageLoading && (
          <CircularProgress
            size={24}
            thickness={4}
            className={classes.spinner}
          />
        )}

        <p className={classes.watermarkRight}>{timestamps[activeStep]}</p>
        <p className={classes.watermarkLeft}>{`${activeStep}/${timestamps.length - 1}`}</p>

        <Zoom in={hoverImg} timeout={{ enter: 1000, exit: 1500 }}>
          <a
            download
            className={classes.download}
            href={imagePaths[activeStep]}
          >
            <Icon className="fa fa-download imgBtn" />
          </a>
        </Zoom>

        <Zoom in={hoverImg} timeout={{ enter: 1000, exit: 1500 }}>
          <span className={classes.play}>
            <Icon
              onClick={() => this.autoPlay()}
              className={autoplayToggled ? 'fa fa-pause imgBtn' : 'fa fa-play imgBtn'}
            />
          </span>
        </Zoom>

        <Zoom in={hoverImg} timeout={200}>
          <div className={classes.arrowRight}>
            <Icon className="fa fa-chevron-right imgBtn" />
          </div>
        </Zoom>

      </div>
    );
  }

  renderImages () {
    const { activeStep } = this.state;
    const { imagePaths, classes } = this.props;
    return imagePaths.map((image, index) => {
      if (image == imagePaths[activeStep]) {
        return <img key="active" className={classes.img} src={image} onLoad={() => this.onLoadImage(index)} />;
      }
      return <img key={image} className={classes.img} src={image} style={{ display: 'none' }} onLoad={() => this.onLoadImage(index)} />;
    });
  }
}

export default withStyles(styles)(ImageViewer);
