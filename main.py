import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.camera import Camera
from viam.components.board import Board
from viam.components.base import Base
from viam.services.vision import VisionClient

import numpy as np
import open3d as o3d

async def connect():
    creds = Credentials(
        type='robot-location-secret',
        payload='3rn6lwpqwh5xzra3sy33x8ul94b5s20zf66ghe6v9bny577z')
    opts = RobotClient.Options(
        refresh_interval=0,
        dial_options=DialOptions(credentials=creds)
    )
    return await RobotClient.at_address('robot7-main.wkhwbmlw2g.viam.cloud', opts)


async def main():
    spinNum = 10  # when turning, spin the motor this much
    straightNum = 300  # when going straight, spin motor this much
    numCycles = 200  # how many times to repeat the main loop
    vel = 500  # go this fast when moving motor

    # Connect to robot client and set up components
    robot = await connect()
    base = Base.from_robot(robot, "base")
    camera = Camera.from_robot(robot, "webcam")

    data, _ = await camera.get_point_cloud()

    # write the point cloud into a temporary file
    with open("/tmp/pointcloud_data.pcd", "wb") as f:
        f.write(data)
    pcd = o3d.io.read_point_cloud("/tmp/pointcloud_data.pcd")
    points = np.asarray(pcd.points)

    print(points)

    # Grab the vision service for the detector
    # detector = VisionClient.from_robot(robot, "happy")

    # # Main loop. Detect the baby
    # for _ in range(numCycles):
    #     # make sure that your camera name in the app matches "my-camera"
    #     detections = await detector.get_detections_from_camera("my-webcam")
    #     found = False
    #     for d in detections:
    #         if d.confidence > 0.8:
    #             if d.class_name.lower() == "baby":
    #                 print(f"Baby found at {d.x}, {d.y}")

    await asyncio.sleep(100)
    await robot.close()

if __name__ == "__main__":
    print("Starting up... ")
    asyncio.run(main())
    print("Done.")
