<html>
	<head>
		<link rel="stylesheet" href="res/style.css" />
		<script src="res/jquery.min.js"></script>
		<script src="res/script.js"></script>
	</head>
	<body>
		<div id="container">
			<div id="header">
				<div id="fiir" class="selected"><h1>FIIR</h1></div>
				<div id="wild"><h1>WILD</h1></div>
				<div id="vip"><h1>VIP</h1></div>
			</div>

			<div id="gallery">
				<?php
					/* for loop here */
					for($i=0; $i<10; $i++){
						$color = "#" . dechex(sprintf('%06d', rand(0,16777215)));
				?>
					
					<div class="frame card">
						<div class="photo" style="background-color:<?php echo $color; ?>"></div>
						<div class="links">
							<a href="#">Instagram link</a>
							<a href="#">Twitter link</a>
						</div>
					</div>

				<?php /* end for loop */	
					}
				?>
			</div>
		</div>
	</body>
</html>
