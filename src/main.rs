use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;

fn main() {
    println!("Hello, world!");
    let file = File::open("data/port1.txt").expect("Un error al abrir el archivo");
    let reader = BufReader::new(file);
    let mut lines = reader.lines().filter_map(Result::ok).peekable();

    let mut n_assets: i32 = 0;

    while let Some(line) = lines.next() {
        if n_assets == 0 {
            n_assets = line.parse().expect("Linea invalida!");
        }

        let asset_data: Vec<f64> = line
            .split_whitespace()
            .filter_map(|x| x.parse().ok())
            .collect();

        print!()

        println!("{}", n_assets);
    }
}

#[derive(Debug)]
struct Asset {
    id: i32,
    mean_return: f64,
    standard_deviation: f64,
}

impl Asset {
    fn new(id: i32, mean_return: f64, standard_deviation: f64) -> Asset {
        Asset {
            id,
            mean_return,
            standard_deviation,
        }
    }
}
