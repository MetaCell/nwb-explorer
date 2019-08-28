import React, { Component } from 'react';
import Icon from '@material-ui/core/Icon';
import Zoom from '@material-ui/core/Zoom';
import { withStyles } from '@material-ui/core/styles';
import CircularProgress from '@material-ui/core/CircularProgress';

const styles = theme => ({
  root: {
    height: "100%",
    display: "flex",
    cursor: "pointer",
    alignItems: "center",
    backgroundColor: "black",
    justifyContent: "space-between",
  },
  img: {
    userSelect: "none",
    height: "100%",
    pointerEvents: "none"
  },
  arrowRight: { 
    opacity: 0.5,
    marginRight: "10px", 
    pointerEvents: "none"
  },
  arrowLeft: { 
    opacity: 0.5,
    marginLeft: "10px",
    pointerEvents: "none"
  },
  watermarkLeft:{
    position: "absolute",
    left: "15px",
    bottom: "5px" 
  },
  watermarkRight:{
    position: "absolute",
    right: "15px",
    bottom: "5px" 
  },
  spinner: {
    color: 'dimgray',
    animationDuration: '550ms',
    position: 'absolute',
    top: "20px",
    right: "13px"
  },
  download: { 
    top: "20px",
    left: "48px",
    opacity: 0.5,
    position: "absolute"
  },
  play: { 
    top: "20px",
    left: "24px",
    opacity: 0.5,
    position: "absolute"
  }

});

class ImageViewer extends Component {
  state = { 
    activeStep: 0,
    imageLoading: true
  };
  cachedImage = []
  headerButtons = ["download", "play", "pause"]
  showNextImage = this.showNextImage.bind(this);
  
  componentDidMount () {
    const { imagePaths } = this.props;
    if (imagePaths === undefined) {
      console.warn("Prop imagePaths in geppetto-client/ImageViewer shouldn't be undefined.")
    } else {
      this.cachedImage = imagePaths.map(() => false)
    }
    
  }

  handleNext = step => {
    const { activeStep } = this.state
    const { timestamps } = this.props

    let nextImageIndex = activeStep + step
    if (nextImageIndex == timestamps.length) {
      nextImageIndex = 0
    } else if (nextImageIndex < 0){
      nextImageIndex = timestamps.length - 1
    }

    this.setState({ 
      activeStep: nextImageIndex, 
      imageLoading: !this.cachedImage[nextImageIndex]
    });
    
  };

  clickImage = (e, num_samples) => {
    const { activeStep } = this.state
    const { offsetX } = e.nativeEvent
    const { offsetWidth } = e.target
    const className = e.target.className
    
    if (!this.headerButtons.some(iconName => className.includes(iconName))) {
      if (offsetX > offsetWidth / 2) {
        this.handleNext(+1)
      } else {
        this.handleNext(-1)
      }
    }
  }

  showNextImage () {
    const { timestamps } = this.props
    const { activeStep } = this.state
    const nextImageIndex = activeStep < timestamps.length - 1 ? activeStep + 1 : 0
    
    this.setState({ 
      activeStep: nextImageIndex,
      imageLoading: !this.cachedImage[nextImageIndex]
    })
  }

  onLoadImage (activeStep, numberOfImages, numberOfImagesToPreload) {
    // hide spinning wheel
    if (!this.cachedImage[activeStep]) {
      this.cachedImage[activeStep] = true
      this.setState({ imageLoading: false })
    }
    // preload next images
    if (activeStep < numberOfImages - numberOfImagesToPreload && !this.cachedImage[activeStep + 1]) {
      const { imagePaths } = this.props
      Array(numberOfImagesToPreload).fill(false).forEach((el, index) => {
        let img = new Image()
        img.src = imagePaths[activeStep + index + 1]
      })
    }
  }

  autoPlay () {
    if (this.interval) {
      clearInterval(this.interval);
      this.interval = null;
    } else {
      this.showNextImage()
      this.interval = setInterval(this.showNextImage, 5000);
    }
    this.setState(({ autoplayToggled }) => ({ autoplayToggled: !autoplayToggled }))
  } 
  
  render () {
    const { imagePaths, timestamps, numberOfImagesToPreload = 1, classes } = this.props;
    const { activeStep, hoverImg, imageLoading, autoplayToggled } = this.state;
    
    return (
      <div 
        className={classes.root}
        onClick={e => this.clickImage(e, timestamps.length)}
        onMouseEnter={() => this.setState({ hoverImg: true })}
        onMouseLeave={() => this.setState({ hoverImg: false })}
      >

        <Zoom in={hoverImg} timeout={200}>
          <div className={classes.arrowLeft}>
            <Icon className='fa fa-chevron-left imgBtn' />
          </div>
        </Zoom>

        <img
          className={classes.img}
          src={imagePaths[activeStep]}
          onLoad={() => this.onLoadImage(activeStep, timestamps.length, numberOfImagesToPreload)}
        />

        {imageLoading && <CircularProgress
          size={24}
          thickness={4}
          className={classes.spinner}
        />}

        <p className={classes.watermarkRight}>{timestamps[activeStep]}</p>
        <p className={classes.watermarkLeft}>{`${activeStep}/${timestamps.length - 1}`}</p>

        <Zoom in={hoverImg} timeout={{ enter: 1000, exit:1500 }}>
          <a download
            className={classes.download} 
            href={imagePaths[activeStep]}
          >
            <Icon className='fa fa-download imgBtn' />
          </a>
        </Zoom>

        <Zoom in={hoverImg} timeout={{ enter: 1000, exit:1500 }}>
          <span className={classes.play}>
            <Icon 
              onClick={() => this.autoPlay()}
              className={autoplayToggled ? 'fa fa-pause imgBtn' : 'fa fa-play imgBtn'}/>
          </span>
        </Zoom>

        <Zoom in={hoverImg} timeout={200}>
          <div className={classes.arrowRight}>
            <Icon className='fa fa-chevron-right imgBtn' />
          </div>
        </Zoom>
        
      </div>
    );
  }
}

export default withStyles(styles)(ImageViewer);
