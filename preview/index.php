<?php
require_once('auth.php');

require_once('get_votes.php');
?><html>
	<head>
		<meta http-equiv="Content-type" content="text/html; charset=utf-8">
		<title>Photos gallery</title>
		<link rel="stylesheet" href="css/gallery.css" type="text/css" />
		<script type="text/javascript" src="js/jquery-1.11.2.min.js"></script>
		<script type="text/javascript" src="js/jquery.history.js"></script>
		<script type="text/javascript" src="js/jquery.galleriffic.js"></script>
		<script type="text/javascript" src="js/jquery.opacityrollover.js"></script>
		<!-- We only want the thumbnails to display when javascript is disabled -->
		<script type="text/javascript">
			document.write('<style>.noscript { display: none; }</style>');
		</script>
	</head>
	<body>
		<div id="page">
			<div id="container">
				<h1><a href="?album=">Photos gallery</a></h1>
				<!--<h2>Integration with history plugin</h2>-->

				<?php if (@$albums_list): ?>
				<h2>Click an album name to display its content.</h2>
				<div id="albums">
					<ul>
						<?php foreach ($albums_list as $album): ?>
						<li>
							<a name="<?php echo htmlspecialchars($album); ?>" href="?album=<?php echo urlencode($album); ?>" title="<?php echo htmlspecialchars($album); ?>">
							<?php echo htmlspecialchars($album); ?>
							</a>
						</li>
						<?php endforeach; ?>
					</ul>
				</div>
				<?php endif; ?>

				<?php if (@$images_list): ?>
				<p>(Click the title to return to albums list)</p><p>&nbsp;</p>
				<!-- Start Advanced Gallery Html Containers -->
				<div id="thumbs" class="navigation">
					<ul class="thumbs noscript">
						<?php foreach ($images_list as $image): ?>
						<li id="image-<?php echo htmlentities($image); ?>">
							<a class="thumb" name="<?php echo htmlspecialchars($image); ?>" href="cache/mediums/<?php echo htmlspecialchars($album); ?>/<?php echo htmlspecialchars($image); ?>" title="<?php echo htmlspecialchars($image); ?>">
								<img src="cache/thumbs/<?php echo htmlspecialchars($album); ?>/<?php echo htmlspecialchars($image); ?>" alt="<?php echo htmlspecialchars($image); ?>" />
							</a>
							<div class="caption">
								<div class="download">
									<a href="originals/<?php echo htmlspecialchars($album); ?>/<?php echo htmlspecialchars($image); ?>">Télécharger <?php echo htmlspecialchars($image); ?></a>
								</div>
								<div class="vote">
									<span class="score <?php if (@$score[$image] < 0) { echo 'score-negative'; } ?>"><?php echo (int)@$score[$image]; ?></span>
									<a onclick="vote(event, this)" href="vote.php?album=<?php echo urlencode($album); ?>&photo=<?php echo urlencode($image); ?>&vote=1"><img src="images/up.png" /></a>
									<a onclick="vote(event, this)" href="vote.php?album=<?php echo urlencode($album); ?>&photo=<?php echo urlencode($image); ?>&vote=-1"><img src="images/down.png" /></a>
								</div>
							</div>
						</li>
						<?php endforeach; ?>

					</ul>
				</div>
				<div id="gallery" class="content">
					<div id="controls" class="controls"></div>
					<div id="caption" class="caption-container"></div>
					<div class="slideshow-container">
						<div id="loading" class="loader"></div>
						<div id="slideshow" class="slideshow"></div>
					</div>
				</div>
				<!-- End Advanced Gallery Html Containers -->
				<?php endif; ?>
				<div style="clear: both;"></div>

				<?php if (@$info_message): ?>
					<div class="info_message"><?php echo $info_message; ?></div>
				<?php endif; ?>

				<?php if (@$html_form) {
					echo $html_form;
				} ?>
			</div>
		</div>
		<!--<div id="footer">&copy; 2009 Trent Foley</div>-->
		<?php if (@$images_list): ?>
		<script type="text/javascript">
			var vote;
			jQuery(document).ready(function($) {
				// We only want these styles applied when javascript is enabled
				//$('div.navigation').css({'width' : '700px', 'float' : 'left'});
				//$('div.content').css('display', 'block');

				// Initially set opacity on thumbs and add
				// additional styling for hover effect on thumbs
				var onMouseOutOpacity = 0.67;
				$('#thumbs ul.thumbs li').opacityrollover({
					mouseOutOpacity:   onMouseOutOpacity,
					mouseOverOpacity:  1.0,
					fadeSpeed:         'fast',
					exemptionSelector: '.selected'
				});
				
				// Initialize Advanced Galleriffic Gallery
				var gallery = $('#thumbs').galleriffic({
					delay:                     2500,
					numThumbs:                 24,
					preloadAhead:              10,
					enableTopPager:            true,
					enableBottomPager:         true,
					maxPagesToShow:            7,
					imageContainerSel:         '#slideshow',
					controlsContainerSel:      '#controls',
					captionContainerSel:       '#caption',
					loadingContainerSel:       '#loading',
					renderSSControls:          true,
					renderNavControls:         true,
					playLinkText:              'Play slideshow',
					pauseLinkText:             'Stop slideshow',
					prevLinkText:              '&lsaquo; Previous photo',
					nextLinkText:              'Next photo &rsaquo;',
					nextPageLinkText:          'Next &rsaquo;',
					prevPageLinkText:          '&lsaquo; Previous',
					enableHistory:             true,
					autoStart:                 false,
					syncTransitions:           true,
					defaultTransitionDuration: 900,
					enableKeyboardNavigation:  false,
					onSlideChange:             function(prevIndex, nextIndex) {
						// 'this' refers to the gallery, which is an extension of $('#thumbs')
						this.find('ul.thumbs').children()
							.eq(prevIndex).fadeTo('fast', onMouseOutOpacity).end()
							.eq(nextIndex).fadeTo('fast', 1.0);

					},
					onPageTransitionOut:       function(callback) {
						this.fadeTo('fast', 0.0, callback);
					},
					onPageTransitionIn:        function() {
						this.fadeTo('fast', 1.0);
					}
				});

				/**** Functions to support integration of galleriffic with the jquery.history plugin ****/

				// PageLoad function
				// This function is called when:
				// 1. after calling $.historyInit();
				// 2. after calling $.historyLoad();
				// 3. after pushing "Go Back" button of a browser
				function pageload(hash) {
					// alert("pageload: " + hash);
					// hash doesn't contain the first # character.
					if(hash) {
						$.galleriffic.gotoImage(hash);
					} else {
						gallery.gotoIndex(0);
					}
				}

				// Initialize history plugin.
				// The callback is called at once by present location.hash. 
				$.historyInit(pageload, "index.php");

				// set onlick event for buttons using the jQuery 1.3 live method
				$("a[rel='history']").on('click', function(e) {
					if (e.button != 0) return true;
					
					var hash = this.href;
					hash = hash.replace(/^.*#/, '');

					// moves to a new page. 
					// pageload is called at once. 
					// hash don't contain "#", "?"
					$.historyLoad(hash);

					return false;
				});

				/****************************************************************************************/


				<?php if (@$images_list): ?>
				/* Score system */
				/*
				jQuery.ajax('get_votes.php', {
					data: {album: "<?php echo str_replace('"', '\\"', $album); ?>"},
					type: 'GET',
					dataType: 'json',
					success: function(data) {
						jQuery('#image-' + image + ' .score').text(0);
						for (var image in data) {
							var score = data[image];
							if (score == undefined) {
								score = 0;
							}
							jQuery('#image-' + image + ' .score').text(score);
							console.info('#image-' + image + ' .score');
							if (score < 0){
								jQuery('#image-' + image + ' .score').addClass('score-negative');
							}
						}
						console.info(jQuery(this));
						console.info(data);
					}
				});
				*/

				vote = function(e, i) {
					e.preventDefault();
					jQuery.ajax(jQuery(i).attr('href'), {
						success: function(data) {
							console.info(jQuery(i).siblings('.score'));
							jQuery(i).siblings('.score').text(data);
							try {
								if (parseInt(data) < 0) {
									jQuery(i).siblings('.score').addClass('score-negative');
								} else {
									jQuery(i).siblings('.score').removeClass('score-negative');
								}
							} catch (ex) { }
						}
					});
				};

				<?php endif; ?>
			});
		</script>
		<?php endif; ?>
	</body>
</html>
