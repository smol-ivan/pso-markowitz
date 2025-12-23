use std::error::Error;
use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() -> Result<(), Box<dyn Error>> {
    let file = File::open("data/port1.txt")?;
    let reader = BufReader::new(file);

    let mut lines = reader.lines().filter_map(Result::ok);

    let fisrt_line = lines.next().ok_or("Bad file")?;

    let n_assets: usize = fisrt_line.trim().parse()?;

    println!("Leyendo {} assets . . .", n_assets);

    let mut assets: Vec<Asset> = Vec::with_capacity(n_assets);

    for (i, line) in lines.take(n_assets).enumerate() {
        let asset_data: Vec<f64> = line
            .split_whitespace()
            .map(|s| s.parse::<f64>())
            .collect::<Result<Vec<_>, _>>()?;

        assets.push(Asset::new(i, asset_data[0], asset_data[1]));
    }

    println!("{:?}", assets.first());

    Ok(())
}

#[derive(Debug)]
struct Asset {
    id: usize,
    mean_return: f64,
    standard_deviation: f64,
}

impl Asset {
    fn new(id: usize, mean_return: f64, standard_deviation: f64) -> Asset {
        Asset {
            id,
            mean_return,
            standard_deviation,
        }
    }
}
