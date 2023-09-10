import asyncio

from viam.robot.client import RobotClient
from viam.rpc.dial import Credentials, DialOptions
from viam.components.camera import Camera
from viam.components.camera import Camera
from viam.components.board import Board
from viam.services.vision import VisionClient


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
    robot = await connect()

    print('Resources:')
    print(robot.resource_names)

    # webcam
    webcam = Camera.from_robot(robot, "webcam")
    webcam_return_value = await webcam.get_image()
    print(f"webcam get_image return value: {webcam_return_value}")

    # transform
    transform = Camera.from_robot(robot, "transform")
    transform_return_value = await transform.get_image()
    print(f"transform get_image return value: {transform_return_value}")

    # Note that the pin supplied is a placeholder. Please change this to a valid pin you are using.
    # local
    local = Board.from_robot(robot, "local")
    local_return_value = await local.gpio_pin_by_name("16")
    print(f"local gpio_pin_by_name return value: {local_return_value}")

    # Note that the Camera supplied is a placeholder. Please change this to a valid Camera.
    # happy
    happy = VisionClient.from_robot(robot, "happy")
    happy_return_value = await happy.get_classifications_from_camera("webcam")
    print(
        f"happy get_classifications_from_camera return value: {happy_return_value}")

    # Don't forget to close the robot when you're done!
    await robot.close()

if __name__ == '__main__':
    asyncio.run(main())


# import asyncio

# from viam.robot.client import RobotClient
# from viam.rpc.dial import Credentials, DialOptions
# from viam.services.vision import VisionServiceClient
# from viam.services.vision import Detection
# from viam.components.camera import Camera
# # from viam.components.base import Base


# async def connect():
#     creds = Credentials(
#         type='robot-location-secret',
#         payload='3rn6lwpqwh5xzra3sy33x8ul94b5s20zf66ghe6v9bny577z')
#     opts = RobotClient.Options(
#         refresh_interval=0,
#         dial_options=DialOptions(credentials=creds)
#     )
#     return await RobotClient.at_address('robot7-main.wkhwbmlw2g.viam.cloud', opts)


# async def main():
#     spinNum = 10  # when turning, spin the motor this much
#     straightNum = 300  # when going straight, spin motor this much
#     numCycles = 200  # how many times to repeat the main loop
#     vel = 500  # go this fast when moving motor

#     # Connect to robot client and set up components
#     robot = await connect()
#     # base = Base.from_robot(robot, "base")
#     camera = Camera.from_robot(robot, "webcam")

#     # Grab the vision service for the detector
#     detector = VisionServiceClient.from_robot(robot, "happy")

#     # Main loop. Detect the baby
#     for _ in range(numCycles):
#         # make sure that your camera name in the app matches "my-camera"
#         detections = await detector.get_detections_from_camera("my-webcam")
#         found = False
#         for d in detections:
#             if d.confidence > 0.8:
#                 if d.class_name.lower() == "baby":
#                     print(f"Baby found at {d.x}, {d.y}")
#     await asyncio.sleep(100)
#     await robot.close()

# if __name__ == "__main__":
#     print("Starting up... ")
#     asyncio.run(main())
#     print("Done.")
