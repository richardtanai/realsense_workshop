import pyrealsense2 as rs
import numpy as np
import cv2


class D435:
    def __init__(self, w = 640, h = 480, fps=30) -> None:
        self.pipeline = rs.pipeline()

        # Create a config and configure the pipeline to stream
        #  different resolutions of color and depth streams
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()


        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        
        profile = self.pipeline.start(config)

        depth_sensor = profile.get_device().first_depth_sensor()

        self.depth_scale = depth_sensor.get_depth_scale()

        align_to = rs.stream.color
        self.align = rs.align(align_to)

        for i in range(60):
            # dump first 60 frames
            frames = self.pipeline.wait_for_frames()


    def get_depth_scale(self):
        return self.depth_scale


    def capture(self):
        # Get frameset of color and depth
        frames = self.pipeline.wait_for_frames()
        # frames.get_depth_frame() is a 640x360 depth image

        # Align the depth frame to color frame
        aligned_frames = self.align.process(frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            pass

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        # images = np.hstack((color_image, depth_colormap))


        # cv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)
        # cv2.imshow('Align Example', images)
        # key = cv2.waitKey(1)
        # key = cv2.waitKey(1)
        # # Press esc or 'q' to close the image window
        # if key & 0xFF == ord('q') or key == 27:
        #     cv2.destroyAllWindows()

        return {"color":color_image, "depth_colormap":depth_colormap}
    

    def capture_color(self):
        # Get frameset of color and depth
        frames = self.pipeline.wait_for_frames()
        # frames.get_depth_frame() is a 640x360 depth image

        # Align the depth frame to color frame
        aligned_frames = self.align.process(frames)

        # Get aligned frames
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid

        color_image = np.asanyarray(color_frame.get_data())

        # images = np.hstack((color_image, depth_colormap))


        # cv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)
        # cv2.imshow('Align Example', images)
        # key = cv2.waitKey(1)
        # key = cv2.waitKey(1)
        # # Press esc or 'q' to close the image window
        # if key & 0xFF == ord('q') or key == 27:
        #     cv2.destroyAllWindows()

        return color_image
    
    def detect_aruco(self):
        img = self.capture()
        color_image = img["color"]
        depth_colormap = img["depth_colormap"]
        
    
    def stop(self):
        self.pipeline.stop()

if __name__ == "__main__":
    myd435 = D435()
    try:
        while True:
            img = myd435.capture()
            color_image = img["color"]
            depth_colormap = img["depth_colormap"]

            images = np.hstack((color_image, depth_colormap))


            cv2.namedWindow('Align Example', cv2.WINDOW_NORMAL)
            cv2.imshow('Align Example', images)
            key = cv2.waitKey(1)
            # Press esc or 'q' to close the image window
            if key & 0xFF == ord('q') or key == 27:
                cv2.destroyAllWindows()
                break
    finally:
        myd435.stop()
