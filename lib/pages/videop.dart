import 'package:appinio_video_player/appinio_video_player.dart';
import 'package:flutter/material.dart';

class VideoP extends StatefulWidget {
  const VideoP({super.key});

  @override
  State<VideoP> createState() => _VideoPState();
}

class _VideoPState extends State<VideoP> {
  late CustomVideoPlayerController _customVideoPlayerController;
  String vOut = "Output.mp4";
  String put = "assets/videos/";

  @override
  void initState() {
    super.initState();
    initializevp();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        title: const Text("Preview"),
      ),
      backgroundColor: const Color.fromARGB(255, 176, 174, 155),
      body: Center(
          child: Column(
        children: [
          Container(
              width: 320,
              color: Colors.black,
              child: CustomVideoPlayer(
                  customVideoPlayerController: _customVideoPlayerController)),
          ElevatedButton(
              onPressed: () => initializevp(), child: const Text("Refresh"))
        ],
      )),
    );
  }

  void initializevp() {
    VideoPlayerController videoPlayerController;
    videoPlayerController = VideoPlayerController.asset(put + vOut)
      ..initialize().then((value) {
        setState(() {});
      });
    _customVideoPlayerController = CustomVideoPlayerController(
        context: context, videoPlayerController: videoPlayerController);
  }

  @override
  void dispose() {
    super.dispose();
  }
}
