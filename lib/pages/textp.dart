// import 'package:edumate2/pages/loading.dart';
// import 'package:flutter/material.dart';

// class Textp extends StatelessWidget {
//   Textp({super.key});

//   final textcon=TextEditingController();

//   @override
//   Widget build(BuildContext context) {
//     return Scaffold(
//       appBar: AppBar(
//         backgroundColor: const Color.fromARGB(255, 176, 174, 155),
//         elevation: 0,
//       ),
//       backgroundColor: const Color.fromARGB(255, 176, 174, 155),
//       body: Center(
//         child:Column(
//           mainAxisAlignment: MainAxisAlignment.start,
//           children: [
//            Padding(
//              padding: const EdgeInsets.only(top: 30),
//              child: Container(
//                decoration: BoxDecoration(borderRadius: BorderRadius.circular(20),color: Colors.white),
//                width: 325,
//                child: TextField(
//                 minLines: 1,
//                 maxLines: 10,
//                 decoration: InputDecoration(border: OutlineInputBorder(borderRadius: BorderRadius.circular(20)),hintText: "Enter the story"),
//                 controller: textcon,
//                ),
//              ),
//            ),
//            Padding(
//              padding: const EdgeInsets.all(15.0),
//              child: ElevatedButton.icon(
//               onPressed: () {
//                 print(textcon.text);
//                 Navigator.push(context, MaterialPageRoute(builder: (context) => const LoadScreen()));
//               }, 
//               label: const Text("Generate"),
//               icon: const Icon(Icons.output),
//               style: const ButtonStyle(
//                 backgroundColor: MaterialStatePropertyAll(Colors.black),
//                 foregroundColor: MaterialStatePropertyAll(Colors.white),
//                 iconSize: MaterialStatePropertyAll(25),
//                 fixedSize: MaterialStatePropertyAll(Size(200, 40)))),
//            )
//           ],
//           ) 
//         ),
//     );
//   }
// }


import 'dart:convert';  // For JSON encoding
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:edumate2/pages/loading.dart';

class Textp extends StatelessWidget {
  Textp({super.key});

  final textcon = TextEditingController();

  // Function to send story to the backend
  Future<void> sendStoryToBackend(String story, BuildContext context) async {
    final url = Uri.parse('http://192.168.213.130:5000/process_story'); // Update with your Flask server URL
    try {
      final response = await http.post(
        url,
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({'story': story}),  // Passing story as JSON
      );

      if (response.statusCode == 200) {
        // print("Story processed successfully");
        Navigator.push(
          context, 
          MaterialPageRoute(builder: (context) => const LoadScreen())
        );
      } else {
        // print("Failed to process story: ${response.statusCode}");
      }
    } catch (e) {
      print("Error: $e");
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color.fromARGB(255, 176, 174, 155),
        elevation: 0,
      ),
      backgroundColor: const Color.fromARGB(255, 176, 174, 155),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            Padding(
              padding: const EdgeInsets.only(top: 30),
              child: Container(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(20),
                  color: Colors.white
                ),
                width: 325,
                child: TextField(
                  minLines: 1,
                  maxLines: 10,
                  decoration: InputDecoration(
                    border: OutlineInputBorder(
                      borderRadius: BorderRadius.circular(20)
                    ),
                    hintText: "Enter the story"
                  ),
                  controller: textcon,
                ),
              ),
            ),
            Padding(
              padding: const EdgeInsets.all(15.0),
              child: ElevatedButton.icon(
                onPressed: () {
                  String story = textcon.text;
                  sendStoryToBackend(story, context);  // Send story to backend
                  Navigator.push(context, MaterialPageRoute(builder: (context) => const LoadScreen())); 
                },
                label: const Text("Generate"),
                icon: const Icon(Icons.output),
                style: const ButtonStyle(
                  backgroundColor: MaterialStatePropertyAll(Colors.black),
                  foregroundColor: MaterialStatePropertyAll(Colors.white),
                  iconSize: MaterialStatePropertyAll(25),
                  fixedSize: MaterialStatePropertyAll(Size(200, 40))
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
