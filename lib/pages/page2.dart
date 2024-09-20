import 'package:edumate2/pages/textp.dart';
import 'package:flutter/material.dart';

class Page2 extends StatelessWidget {
  const Page2({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color.fromARGB(255, 176, 174, 155),
      appBar: AppBar(
        backgroundColor: const Color.fromARGB(255, 176, 174, 155),
        actions: [
          IconButton(
              onPressed: () {}, icon: const Icon(Icons.info_outline_rounded))
        ],
      ),
      body: Center(
        child: Padding(
          padding: const EdgeInsets.all(80),
          child: Column(
            children: [
              GestureDetector(
                onTap: () {
                  Navigator.push(context,
                      MaterialPageRoute(builder: (context) => Textp()));
                },
                child: Padding(
                  padding: const EdgeInsets.all(15),
                  child: Container(
                    height: 50,
                    width: 230,
                    decoration: BoxDecoration(
                        color: Colors.black,
                        borderRadius: BorderRadius.circular(10)),
                    child: const Center(
                      child: Text(
                        "Upload Text",
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 20,
                        ),
                      ),
                    ),
                  ),
                ),
              ),
              GestureDetector(
                onTap: () {
                  Navigator.push(context,
                      MaterialPageRoute(builder: (context) => Textp()));
                },
                child: Padding(
                  padding: const EdgeInsets.all(15),
                  child: Container(
                    height: 50,
                    width: 230,
                    decoration: BoxDecoration(
                        color: Colors.black,
                        borderRadius: BorderRadius.circular(10)),
                    child: const Center(
                      child: Text(
                        "Upload Image",
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 20,
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
