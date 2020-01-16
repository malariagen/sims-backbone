package net.malariagen.sims.lims;

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVPrinter;

import com.amazonaws.services.lambda.runtime.Context;
import com.amazonaws.services.lambda.runtime.LambdaLogger;
import com.amazonaws.services.lambda.runtime.RequestHandler;
import com.amazonaws.services.lambda.runtime.events.S3Event;
import com.amazonaws.services.s3.AmazonS3;
import com.amazonaws.services.s3.AmazonS3ClientBuilder;
import com.amazonaws.services.s3.event.S3EventNotification.S3EventNotificationRecord;
import com.amazonaws.services.s3.model.GetObjectRequest;
import com.amazonaws.services.s3.model.ObjectMetadata;
import com.amazonaws.services.s3.model.S3Object;
import com.amazonaws.util.IOUtils;

public class Transform implements RequestHandler<S3Event, String> {

	public String handleRequest(S3Event event, Context context) {
		LambdaLogger logger = context.getLogger();

		try {
			S3EventNotificationRecord record = event.getRecords().get(0);

			String srcBucket = record.getS3().getBucket().getName();
			// Object key may have spaces or unicode non-ASCII characters.
			String srcKey = record.getS3().getObject().getKey().replace('+', ' ');
			srcKey = URLDecoder.decode(srcKey, "UTF-8");

			String dstBucket = srcBucket;
			String dstKey = srcKey + ".csv";

			// Download the image from S3 into a stream
			AmazonS3 s3Client = AmazonS3ClientBuilder.defaultClient();
			S3Object s3Object = s3Client.getObject(new GetObjectRequest(srcBucket, srcKey));
			InputStream objectData = s3Object.getObjectContent();
			// Re-encode image to target format
			ByteArrayOutputStream os = new ByteArrayOutputStream();
			this.createCSV(objectData, os);

			InputStream is = new ByteArrayInputStream(os.toByteArray());
			// Set Content-Length and Content-Type
			ObjectMetadata meta = new ObjectMetadata();
			meta.setContentLength(os.size());
			// Uploading to S3 destination bucket
			System.out.println("Writing to: " + dstBucket + "/" + dstKey);
			s3Client.putObject(dstBucket, dstKey, is, meta);
			System.out.println("Successfully resized " + srcBucket + "/" + srcKey + " and uploaded to " + dstBucket
					+ "/" + dstKey);
			logger.log("Spare time available is:" + context.getRemainingTimeInMillis());
			return "Ok";
		} catch (IOException e) {
			throw new RuntimeException(e);
		}

	}

	private void createCSV(InputStream inputStream, OutputStream outputStream)
			throws IOException, UnsupportedEncodingException {

		File tempFile = File.createTempFile("lims-sims", ".accdb");

		FileOutputStream tempStream = new FileOutputStream(tempFile);

		IOUtils.copy(inputStream, tempStream);

		System.err.print("Temp file size is:" + tempFile.length());

		try {
			Connection conn = DriverManager.getConnection("jdbc:ucanaccess://" + tempFile.getCanonicalPath());

			OutputStreamWriter writer = new OutputStreamWriter(outputStream, "UTF-8");

			CSVPrinter csvPrinter = new CSVPrinter(writer, CSVFormat.TDF.withHeader("calc_study_code",
					"study.study_code", "plate.study_code as plate_study_code", "study.study_species", "roma_code",
					"oxford_code", "external_id", "sample.sample_code", "batch.arrived", "plate.plate_code",
					"plate.plate_barcode", "plate.plate_comment", "plate_well_contents", "well.well_id", "well.well",
					"well.derivative_sample_id", "well.updated_on", "parent_well.derivative_sample_id as parent_id",
					"sanger_manifest_ids.sanger_sample_id", "sanger_manifest_ids.entered_on",
					"sanger_manifest_ids.sanger_plate_id", "sanger_manifest_ids.sanger_plate_barcode", "position_name",
					"stack_name", "rack_name", "shelf_code", "freezer_code"));

			Statement stmt = conn.createStatement();
			ResultSet rs = stmt.executeQuery(
					"select study.study_code, plate.study_code as plate_study_code, study.study_species, sample.sample_code,batch.arrived, plate.plate_code, plate.plate_barcode, plate.plate_comment, plate_well_contents, well.well_id, well.well, well.derivative_sample_id, well.updated_on, parent_well.derivative_sample_id as parent_id, sanger_manifest_ids.sanger_sample_id, sanger_manifest_ids.entered_on, sanger_manifest_ids.sanger_plate_id, sanger_manifest_ids.sanger_plate_barcode, position_name, stack_name, rack_name, shelf_code, freezer_code\n"
							+ "  FROM sample\n" + "	LEFT JOIN batch ON sample.batch_id = batch.batch_id\n"
							+ "	LEFT JOIN well ON well.sample_id = sample.sample_id\n"
							+ "	LEFT JOIN plate ON plate.plate_id = well.plate_id\n"
							+ "	LEFT JOIN plate_well_contents ON plate_well_contents.plate_well_contents_id = plate.plate_well_contents_id\n"
							+ "	LEFT JOIN batch_study ON batch_study.batch_id = batch.batch_id\n"
							+ "	LEFT JOIN study ON study.study_id = batch_study.study_id\n"
							+ "	LEFT JOIN well as parent_well ON parent_well.well_id = well.from_well_id \n"
							+ "	LEFT JOIN sanger_manifest_ids ON sanger_manifest_ids.well_id = well.well_id\n"
							+ "	LEFT JOIN `position` pos ON pos.plate_id = plate.plate_id\n"
							+ "	LEFT JOIN stack ON pos.stack_id = stack.stack_id\n"
							+ "	LEFT JOIN rack ON rack.rack_id = stack.rack_id\n"
							+ "	LEFT JOIN shelf ON shelf.shelf_id = rack.shelf_id\n"
							+ "	LEFT JOIN freezer ON freezer.freezer_id = shelf.freezer_id\n" + "");
			while (rs.next()) {

				String study_code = rs.getString("study_code");
				String plate_study_code = rs.getString("plate_study_code");
				String calc_study_code = "";
				String s_code = "";
				String p_code = "";
				Pattern pattern = Pattern.compile("^([\\d]{4}).*");
				// System.out.println(study_code + " " + plate_study_code);

				if (study_code != null) {
					Matcher matcher = pattern.matcher(study_code);
					if (matcher.matches()) {
						s_code = matcher.group(1);

					}
				}
				if (plate_study_code != null) {
					Matcher pmatcher = pattern.matcher(plate_study_code);
					if (pmatcher.matches()) {
						p_code = pmatcher.group(1);
					}
				}

				String sample_code = rs.getString("sample.sample_code");

				// System.out.println(s_code + " " + p_code);
				if (s_code.equals("0000") || s_code.length() == 0) {
					calc_study_code = p_code;
				} else if (!s_code.equals(p_code) && p_code.length() > 0) {
					System.out.println("Study codes don't match: " + sample_code + " " + s_code + " " + p_code);
					// Usually seems to be right...
					calc_study_code = s_code;
				} else {
					calc_study_code = s_code;
				}
				// System.out.println(calc_study_code);
				String roma_code = "";
				String oxford_code = "";
				String external_id = "";
				Pattern roma_pattern = Pattern.compile("^(SPT|RCN|VVX|VBS)([\\d]{5}).*");
				// System.out.println(study_code + " " + plate_study_code);
				Matcher rmatcher = roma_pattern.matcher(sample_code);

				if (rmatcher.matches()) {
					roma_code = rmatcher.group(1) + rmatcher.group(2);

				} else {
					Pattern oxf_pattern = Pattern.compile("^([\\p{Lu}]{2})([\\d]{4})(-)(C|Cx|Cw)");
					// System.out.println(study_code + " " + plate_study_code);
					Matcher omatcher = oxf_pattern.matcher(sample_code);
					if (omatcher.matches()) {
						oxford_code = omatcher.group(0);
					} else {
						if (!(sample_code.equals("EMPTY") || sample_code.equals("BLANK"))) {
							external_id = sample_code;
						} else {
							// Not ignored as used to keep db tidy i.e. all wells in a plate
						}
					}
				}

				csvPrinter.printRecord(calc_study_code, rs.getString("study_code"), rs.getString("plate_study_code"),
						rs.getString("study.study_species"), roma_code, oxford_code, external_id,
						rs.getString("sample.sample_code"), rs.getDate("batch.arrived"), rs.getString("plate_code"),
						rs.getString("plate_barcode"), rs.getString("plate_comment"),
						rs.getString("plate_well_contents"), rs.getString("well_id"), rs.getString("well"), rs.getString("derivative_sample_id"),
						rs.getString("well.updated_on"), rs.getString("parent_id"), rs.getString("sanger_sample_id"),
						rs.getString("entered_on"), rs.getString("sanger_plate_id"),
						rs.getString("sanger_plate_barcode"), rs.getString("position_name"), rs.getString("stack_name"),
						rs.getString("rack_name"), rs.getString("shelf_code"), rs.getString("freezer_code"));
			}

			conn.close();

			csvPrinter.flush();
			csvPrinter.close();

		} catch (

		SQLException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		tempFile.delete();
	}

	/**
	 * Usage:
	 * java -jar lims-sims/target/lims-transform-1.0-SNAPSHOT.jar net.malariagen.sims.lims.Transform ./input/import/access/lab_sam_track_db_tables_20191014.accdb ./input/import/access/lab_sam_track_db_tables_20191014.accdb.csv
	 * @param args
	 */
	public static void main(String[] args) {
		Transform t = new Transform();

		try {
			File directory = new File(args[1]);
			   System.out.println(directory.getAbsolutePath());
			FileInputStream fis = new FileInputStream(args[1]);
			File fout = new File(args[2]);
			if (fout.exists()) {
				fout.delete();
			}
			fout.createNewFile();
			FileOutputStream fos = new FileOutputStream(fout);

			t.createCSV(fis, fos);
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (UnsupportedEncodingException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}

	}
}
